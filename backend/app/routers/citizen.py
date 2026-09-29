import hashlib
import time
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func,cast,select
from geoalchemy2 import Geography
from app.db.base import get_db
from app.db.models.users import UserRole,Consent,uid,now
from app.db.models.needs import Need,NeedStatus,Evidence,NeedEvent,PipelineRun
from app.schemas.needs import NeedCreate,AnalyzeRequest
from app.core.rbac import require_role,get_current_user,PLANNERS,in_scope
from app.core.storage import validate_media,put_media,read_media
from app.services.ai_service import analyze,redact
from app.services.geocoding import reverse
from app.services.audit import audit

router=APIRouter()
reporter=require_role([UserRole.citizen,UserRole.volunteer])

def serialize(db,need,detail=False):
    lon,lat=db.query(func.ST_X(Need.location),func.ST_Y(Need.location)).filter(Need.id==need.id).one()
    result={k:getattr(need,k) for k in ("id","is_sample","category","description","affected_people","address","state","district","locality","ward_village","status","created_at","updated_at","language","geocoding_source","project_id")}
    result.update(latitude=lat,longitude=lon)
    if detail:
        result["events"]=[{"status":e.status,"created_at":e.created_at} for e in need.events]
        result["evidence"]=[{"id":e.id,"content_type":e.content_type,"size_bytes":e.size_bytes,"anonymized":e.anonymized} for e in need.evidence]
    return result

def own(db,id,user):
    need=db.get(Need,id)
    if not need or need.reported_by_id!=user.id: raise HTTPException(404,"not_found")
    return need

def create_need(db,data,user):
    if user.role==UserRole.volunteer and not data.citizen_consent:
        raise HTTPException(400,"citizen_consent_required")
    payload_hash=hashlib.sha256(data.model_dump_json().encode()).hexdigest()
    # Serialize retries for a user's offline batch across processes.
    lock=int(hashlib.sha256((user.id+data.client_id).encode()).hexdigest()[:15],16)
    db.execute(__import__('sqlalchemy').text("SELECT pg_advisory_xact_lock(:key)"),{"key":lock})
    existing=db.query(Need).filter_by(reported_by_id=user.id,client_id=data.client_id).first()
    if existing:
        if existing.payload_hash!=payload_hash: raise HTTPException(409,"idempotency_conflict")
        return existing
    active=db.query(Consent).filter_by(user_id=user.id,purpose="account_and_reporting",status="active").first()
    if not active: raise HTTPException(403,"consent_required")
    if data.project_id:
        from app.db.models.projects import Project
        if not db.get(Project,data.project_id): raise HTTPException(404,"not_found")
    consent=Consent(user_id=user.id,purpose="assisted_report" if user.role==UserRole.volunteer else "report",
                    language=data.language,channel="volunteer" if user.role==UserRole.volunteer else "web")
    db.add(consent);db.flush()
    started=time.perf_counter();geo=reverse(round(data.latitude,5),round(data.longitude,5))
    need=Need(id=uid(),category=data.category,description=redact(data.description),
        affected_people=data.affected_people,location=f"SRID=4326;POINT({data.longitude} {data.latitude})",
        address=data.address or geo["address"],state=data.state.strip(),district=data.district.strip(),
        locality=data.locality,ward_village=data.ward_village,reported_by_id=user.id,consent_id=consent.id,
        project_id=data.project_id,client_id=data.client_id,payload_hash=payload_hash,geocoding_source=geo["source"])
    db.add(need);db.flush()
    db.add(PipelineRun(need_id=need.id,stage="geocoding",model_version="nominatim-reverse-1",
        latency_ms=(time.perf_counter()-started)*1000,success=geo["source"]=="openstreetmap"))
    result=analyze(data.description,db,need.id);need.language=result["language"]
    duplicate=db.query(Need).filter(Need.id!=need.id,Need.description==need.description,Need.state==need.state,Need.district==need.district).first()
    if duplicate: need.moderation_reason="duplicate"
    elif result["category"]=="other": need.moderation_reason="classification_uncertainty"
    db.add(NeedEvent(need_id=need.id,status="reported"))
    audit(db,user,"need.created",need.id)
    return need

@router.post("/analyze")
def understanding(data:AnalyzeRequest,user=Depends(reporter),db:Session=Depends(get_db)):
    result=analyze(data.description,db)
    db.commit()
    return result

@router.get("/geocode")
def geocode(latitude:float=Query(ge=-90,le=90),longitude:float=Query(ge=-180,le=180),user=Depends(reporter)):
    return reverse(round(latitude,5),round(longitude,5))

@router.post("/needs")
def report(data:NeedCreate,user=Depends(reporter),db:Session=Depends(get_db)):
    need=create_need(db,data,user);db.commit()
    return serialize(db,need,True)

@router.get("/needs")
def requests(status:NeedStatus|None=None,sort:str="newest",user=Depends(reporter),db:Session=Depends(get_db)):
    query=db.query(Need).filter(Need.reported_by_id==user.id)
    if status:query=query.filter(Need.status==status)
    query=query.order_by(Need.created_at.asc() if sort=="oldest" else Need.created_at.desc())
    return [serialize(db,n) for n in query.limit(500).all()]

@router.get("/needs/nearby")
def nearby(lat:float=Query(ge=-90,le=90),lng:float=Query(ge=-180,le=180),radius_km:float=Query(default=5,gt=0,le=50),user=Depends(reporter),db:Session=Depends(get_db)):
    point=func.ST_SetSRID(func.ST_MakePoint(lng,lat),4326)
    distance=func.ST_Distance(cast(Need.location,Geography),cast(point,Geography))
    rows=db.query(Need,distance).filter(func.ST_DWithin(cast(Need.location,Geography),cast(point,Geography),radius_km*1000)).order_by(distance).limit(100).all()
    # Aggregated public-facing metadata only; no raw descriptions or identities.
    return [{"id":n.id,"category":n.category,"status":n.status,"district":n.district,"distance_meters":d} for n,d in rows]

@router.get("/needs/{id}")
def detail(id:str,user=Depends(reporter),db:Session=Depends(get_db)):
    return serialize(db,own(db,id,user),True)

@router.post("/needs/{id}/media")
async def upload(id:str,file:UploadFile=File(...),user=Depends(reporter),db:Session=Depends(get_db)):
    need=own(db,id,user)
    report_consent=db.get(Consent,need.consent_id)
    active=db.query(Consent).filter_by(user_id=user.id,purpose="account_and_reporting",status="active").first()
    if not active or not report_consent or report_consent.status!="active":raise HTTPException(403,"consent_required")
    from app.core.config import settings
    raw=await file.read(settings.MAX_UPLOAD_BYTES+1)
    raw,ctype,suffix=validate_media(raw,file.content_type)
    db.execute(__import__('sqlalchemy').text("SELECT pg_advisory_xact_lock(:key)"),{"key":int(hashlib.sha256(id.encode()).hexdigest()[:15],16)})
    digest=hashlib.sha256(id.encode()+raw).hexdigest()
    key=f"evidence/{user.id}/{digest}{suffix}"
    existing=db.query(Evidence).filter_by(need_id=id,file_url=key).first()
    if existing:return {"id":existing.id,"content_type":existing.content_type}
    if db.query(Evidence).filter_by(need_id=id).count()>=5:raise HTTPException(400,"media_count_limit")
    put_media(key,raw,ctype)
    evidence=Evidence(need_id=id,file_url=key,uploaded_by_id=user.id,content_type=ctype,size_bytes=len(raw),anonymized=False)
    db.add(evidence);audit(db,user,"evidence.uploaded",id);db.commit()
    return {"id":evidence.id,"content_type":ctype}

@router.get("/media/{id}")
def media(id:str,user=Depends(get_current_user),db:Session=Depends(get_db)):
    e=db.get(Evidence,id);n=db.get(Need,e.need_id) if e else None
    allowed=n and (n.reported_by_id==user.id or user.role==UserRole.admin or
        (user.role==UserRole.volunteer and user.state==n.state and user.district==n.district) or
        (user.role in PLANNERS and in_scope(n,user)))
    if not allowed:raise HTTPException(404,"not_found")
    response=read_media(e.file_url)
    try:return Response(response.read(),media_type=e.content_type,headers={"Cache-Control":"private, no-store","X-Content-Type-Options":"nosniff"})
    finally:response.close();response.release_conn()
