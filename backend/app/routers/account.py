from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from typing import Literal
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.users import Consent,now
from app.db.models.needs import Need,NeedEvent
from app.core.rbac import get_current_user
from app.services.audit import audit

router=APIRouter()
def consent_view(c):
    return {k:getattr(c,k) for k in ("id","user_id","purpose","language","channel","version","status","recorded_at","withdrawn_at")}
@router.get("/consents")
def consents(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return [consent_view(c) for c in db.query(Consent).filter_by(user_id=user.id).order_by(Consent.recorded_at.desc())]
class Choice(BaseModel):
    status:Literal["active","withdrawn"]
@router.patch("/consents/{id}")
def consent(id:str,data:Choice,user=Depends(get_current_user),db:Session=Depends(get_db)):
    c=db.get(Consent,id)
    if not c or c.user_id!=user.id:raise HTTPException(404,"not_found")
    c.status=data.status;c.withdrawn_at=now() if data.status=="withdrawn" else None
    audit(db,user,"consent."+data.status,c.id);db.commit()
    return consent_view(c)
@router.get("/notifications")
def notifications(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return [{"id":e.id,"need_id":n.id,"category":n.category,"status":e.status,"created_at":e.created_at} for e,n in db.query(NeedEvent,Need).join(Need,Need.id==NeedEvent.need_id).filter(Need.reported_by_id==user.id).order_by(NeedEvent.created_at.desc()).limit(100)]


from pydantic import Field
from app.core.security import verify_password,get_password_hash
from app.core.storage import get_minio_client
from app.core.config import settings
from app.db.models.users import AccessRequest,UserStatus,UserRole,uid
from app.db.models.needs import Evidence
from app.db.models.projects import ModerationNote
from sqlalchemy import func
class Erase(BaseModel):
    password:str=Field(min_length=1,max_length=72)
    confirm:Literal[True]
@router.post("/erase")
def erase(data:Erase,user=Depends(get_current_user),db:Session=Depends(get_db)):
    if user.role==UserRole.admin:raise HTTPException(400,"admin_status_protected")
    if not verify_password(data.password,user.password_hash):raise HTTPException(401,"invalid_credentials")
    needs=db.query(Need).filter_by(reported_by_id=user.id).all()
    for n in needs:
        for e in db.query(Evidence).filter_by(need_id=n.id).all():
            try:
                client=get_minio_client();client.remove_object(settings.MINIO_BUCKET,e.file_url)
                if e.public_file_url:client.remove_object(settings.MINIO_BUCKET,e.public_file_url)
            except Exception:raise HTTPException(503,"storage_unavailable")
            db.delete(e)
        db.query(ModerationNote).filter_by(need_id=n.id).delete(synchronize_session=False)
        n.description="[erased]";n.address=None;n.reported_by_id=None;n.affected_people=None
        n.locality="";n.ward_village="";n.payload_hash=None;n.client_id=None;n.status="rejected";n.moderation_reason=None
        n.location=func.ST_SnapToGrid(Need.location,1)
    for c in db.query(Consent).filter_by(user_id=user.id):c.status="withdrawn";c.withdrawn_at=now()
    application=db.query(AccessRequest).filter_by(user_id=user.id).first()
    if application:
        application.organization="[erased]";application.designation="";application.reason="";application.verification_info=""
    user.name="[erased]";user.email=None;user.mobile=None;user.locality=None;user.ward_village=None
    user.state=None;user.district=None;user.password_hash=get_password_hash(uid());user.status=UserStatus.suspended;user.token_version+=1
    audit(db,user,"account.erased",user.id);db.commit()
    return {"message":"account_erased"}
