from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel,Field
from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import func,text,select
from app.db.base import get_db
from app.db.models.users import User,UserRole,Consent,AuditLog,now
from app.db.models.needs import Need,NeedEvent,Evidence
from app.db.models.projects import IntegrationStatus,ModerationNote
from app.core.rbac import require_role,GOVERNANCE
from app.routers.account import consent_view
from app.services.audit import audit
from app.core.storage import get_minio_client
router=APIRouter()
admin=require_role([UserRole.admin])
reader=require_role(GOVERNANCE)
@router.get("/overview")
@router.get("/reports")
def overview(user=Depends(admin),db:Session=Depends(get_db)):
    return {"users":db.query(User).count(),"pending_approval":db.query(User).filter_by(status="pending_approval").count(),
        "requests":db.query(Need).count(),"review_required":db.query(Need).filter(Need.moderation_reason.isnot(None)).count(),
        "active_consents":db.query(Consent).filter_by(status="active").count(),
        "statuses":[{"status":s.value,"count":c} for s,c in db.query(Need.status,func.count(Need.id)).group_by(Need.status)]}
@router.get("/roles")
def roles(user=Depends(admin)):
    return [{"role":r.value,"permissions":p} for r,p in [
        (UserRole.citizen,["own_reports","own_profile","own_consent"]),
        (UserRole.volunteer,["own_reports","district_verification","offline_sync"]),
        (UserRole.district_official,["district_planning"]),
        (UserRole.state_planner,["state_planning"]),
        (UserRole.national_planner,["national_planning"]),
        (UserRole.auditor,["read_audit","read_pipeline_metrics"]),
        (UserRole.admin,["approve_accounts","moderate_requests","withdraw_consent","read_audit","read_pipeline_metrics"])]]
@router.get("/requests")
def requests(review:bool=False,user=Depends(admin),db:Session=Depends(get_db)):
    q=db.query(Need)
    if review:q=q.filter(Need.moderation_reason.isnot(None))
    return [{k:getattr(n,k) for k in ("id","category","state","district","status","moderation_reason","created_at")} for n in q.order_by(Need.created_at.desc()).limit(500)]
class Moderate(BaseModel):
    action:Literal["clear_review","reject"]
    note:str=Field(min_length=3,max_length=1000)
@router.patch("/requests/{id}")
def moderate(id:str,data:Moderate,user=Depends(admin),db:Session=Depends(get_db)):
    n=db.scalar(select(Need).where(Need.id==id).with_for_update())
    if not n:raise HTTPException(404,"not_found")
    if n.status.value in ("resolved","rejected"):raise HTTPException(409,"invalid_transition")
    db.add(ModerationNote(need_id=n.id,actor_id=user.id,note=data.note))
    n.moderation_reason=None;n.updated_at=now()
    if data.action=="reject":
        n.status="rejected";db.add(NeedEvent(need_id=n.id,status="rejected"))
    audit(db,user,"moderation."+data.action,n.id);db.commit()
    return {"status":n.status}
@router.get("/consent")
def consents(user=Depends(admin),db:Session=Depends(get_db)):
    return [consent_view(c) for c in db.query(Consent).order_by(Consent.recorded_at.desc()).limit(500)]
class Withdraw(BaseModel):
    status:Literal["withdrawn"]
@router.patch("/consent/{id}")
def withdraw(id:str,data:Withdraw,user=Depends(admin),db:Session=Depends(get_db)):
    c=db.get(Consent,id)
    if not c:raise HTTPException(404,"not_found")
    c.status="withdrawn";c.withdrawn_at=now();audit(db,user,"consent.withdrawn",c.id);db.commit()
    return consent_view(c)
@router.get("/audit-logs")
def logs(action:str="",limit:int=Query(default=100,ge=1,le=500),user=Depends(reader),db:Session=Depends(get_db)):
    q=db.query(AuditLog)
    if action:q=q.filter(AuditLog.action==action)
    return [{k:getattr(a,k) for k in ("id","timestamp","actor_id","role","action","resource","result")} for a in q.order_by(AuditLog.timestamp.desc()).limit(limit)]
@router.get("/integrations")
def integrations(user=Depends(admin),db:Session=Depends(get_db)):
    return [{"name":i.name,"status":i.status} for i in db.query(IntegrationStatus).order_by(IntegrationStatus.name)]
@router.get("/health")
def health(user=Depends(admin),db:Session=Depends(get_db)):
    db.execute(text("SELECT 1"))
    try:get_minio_client().list_buckets();storage="available"
    except Exception:storage="unavailable"
    restricted=not db.scalar(text("SELECT has_table_privilege(current_user,'audit_logs','UPDATE') OR has_table_privilege(current_user,'audit_logs','DELETE') OR has_table_privilege(current_user,'audit_logs','TRUNCATE')"))
    return {"database":"available","storage":storage,"audit_permissions":"restricted" if restricted else "owner_connection_requires_runtime_role"}
@router.get("/data-governance")
def data_governance(user=Depends(admin),db:Session=Depends(get_db)):
    return {"private_media":db.query(Evidence).count(),"public_media":eligible(db).count(),
        "policy":"Original evidence is private. Reviewed redacted images may be public while reporting consent remains active. Audit logs are append-only."}


from fastapi import UploadFile,File,Form
from app.routers.citizen import serialize
from app.core.storage import validate_media,put_media
from app.core.config import settings
from app.services.public_evidence import eligible
@router.get("/requests/{id}")
def request_detail(id:str,user=Depends(admin),db:Session=Depends(get_db)):
    n=db.get(Need,id)
    if not n:raise HTTPException(404,"not_found")
    return serialize(db,n,True)
@router.post("/evidence/{id}/publish")
async def publish(id:str,file:UploadFile=File(...),reviewed:bool=Form(...),user=Depends(admin),db:Session=Depends(get_db)):
    e=db.get(Evidence,id);n=db.get(Need,e.need_id) if e else None
    if not n or not n.project_id:raise HTTPException(404,"not_found")
    c=db.get(Consent,n.consent_id)
    active=db.query(Consent).filter_by(user_id=n.reported_by_id,purpose="account_and_reporting",status="active").first()
    if not reviewed or not c or c.status!="active" or not active:raise HTTPException(403,"consent_required")
    if file.content_type not in ("image/jpeg","image/png","image/webp"):raise HTTPException(400,"unsupported_media")
    raw,ctype,suffix=validate_media(await file.read(settings.MAX_UPLOAD_BYTES+1),file.content_type)
    key="public-evidence/"+e.id+suffix
    put_media(key,raw,ctype);e.public_file_url=key;e.anonymized=True
    audit(db,user,"evidence.public_reviewed",e.id);db.commit()
    return {"id":e.id,"source_badge":"Citizen Submitted"}
