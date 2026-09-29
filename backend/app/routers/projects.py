from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import func,cast,or_,String
from sqlalchemy.orm import Session
from geoalchemy2 import Geography
from app.db.base import get_db
from app.db.models.projects import Project,ProjectEvent
from app.db.models.needs import Need,Evidence
from app.services.public_evidence import eligible
from app.core.storage import read_media
from fastapi.responses import Response

router=APIRouter()
FIELDS=("name","category","state","district","locality","ward_village","department","contractor","sanctioned_cost","actual_cost","planned_start","planned_completion","actual_start","actual_completion","responsible_agency","responsible_official","office_contact","department_chain","status","progress")
BADGES={"Synthetic Sample","Verified Source","Citizen Submitted","Government Dataset","Integrated Dataset","User supplied — unverified"}
def summary(db,p):
    lon,lat=db.query(func.ST_X(Project.location),func.ST_Y(Project.location)).filter(Project.id==p.id).one()
    return {**{k:getattr(p,k) for k in ("id","name","category","state","district","status","progress","is_sample")},"latitude":lat,"longitude":lon,"has_dataset":p.dataset_record is not None}
@router.get("/search")
def search(q:str=Query(default="",max_length=150),state:str="",district:str="",category:str="",lat:float|None=Query(default=None,ge=-90,le=90),lng:float|None=Query(default=None,ge=-180,le=180),radius_km:float=Query(default=25,gt=0,le=200),db:Session=Depends(get_db)):
    query=db.query(Project)
    if q:
        pattern="%"+q.replace("\\","\\\\").replace("%","\\%").replace("_","\\_")+"%"
        columns=[getattr(Project,k) for k in ("id","name","state","district","locality","department","contractor")]
        query=query.filter(or_(*[column.ilike(pattern,escape="\\") for column in columns],cast(Project.dataset_record,String).ilike(pattern,escape="\\")))
    for key,value in (("state",state),("district",district),("category",category)):
        if value:query=query.filter(getattr(Project,key)==value)
    if (lat is None)!=(lng is None):raise HTTPException(422,"validation_error")
    if lat is not None:
        point=func.ST_SetSRID(func.ST_MakePoint(lng,lat),4326)
        query=query.filter(func.ST_DWithin(cast(Project.location,Geography),cast(point,Geography),radius_km*1000))
    return [summary(db,p) for p in query.order_by(Project.name).limit(100)]
@router.get("/{id}")
def detail(id:str,db:Session=Depends(get_db)):
    p=db.get(Project,id)
    if not p:raise HTTPException(404,"not_found")
    result=summary(db,p)
    result["dataset_record"]=p.dataset_record
    result["fields"]={}
    for key in FIELDS:
        value=getattr(p,key)
        source=(p.source_badges or {}).get(key)
        badge=source if source in BADGES and value is not None and value!="" else "Information Not Available"
        result["fields"][key]={"value":value if badge!="Information Not Available" else None,"source_badge":badge}
    result["timeline"]=[{"stage":e.stage,"occurred_at":e.occurred_at,"source_badge":(p.source_badges or {}).get("timeline","Information Not Available")} for e in db.query(ProjectEvent).filter_by(project_id=id).order_by(ProjectEvent.occurred_at)]
    # Raw citizen media is deliberately excluded: the current pipeline cannot guarantee anonymization.
    result["evidence"]=[{"id":e.id,"source_badge":"Citizen Submitted"} for e in eligible(db).filter(Need.project_id==id)]
    return result


@router.get("/evidence/{id}/media")
def public_media(id:str,db:Session=Depends(get_db)):
    e=eligible(db).filter(Evidence.id==id).first()
    if not e:raise HTTPException(404,"not_found")
    response=read_media(e.public_file_url)
    try:return Response(response.read(),media_type="image/jpeg",headers={"Cache-Control":"no-store","X-Content-Type-Options":"nosniff"})
    finally:response.close();response.release_conn()
