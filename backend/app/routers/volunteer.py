from datetime import timedelta
from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel,Field
from typing import Literal
from sqlalchemy import func,cast,select
from sqlalchemy.orm import Session
from geoalchemy2 import Geography
from app.db.base import get_db
from app.db.models.users import UserRole,now
from app.db.models.needs import Need,NeedStatus,NeedEvent
from app.core.rbac import require_role
from app.schemas.needs import BatchNeeds
from app.routers.citizen import serialize,create_need
from app.services.audit import audit
router=APIRouter()
volunteer=require_role([UserRole.volunteer])

@router.get("/stats")
def stats(user=Depends(volunteer),db:Session=Depends(get_db)):
    return {"captured":db.query(Need).filter_by(reported_by_id=user.id).count(),
        "pending_verification":db.query(Need).filter_by(state=user.state,district=user.district,status=NeedStatus.reported).count(),
        "verified_today":db.query(Need).filter(Need.verified_by_id==user.id,Need.verified_at>=now().replace(hour=0,minute=0,second=0,microsecond=0)).count()}

@router.get("/tasks")
def tasks(lat:float|None=Query(default=None,ge=-90,le=90),lng:float|None=Query(default=None,ge=-180,le=180),
    radius_km:float=Query(default=15,gt=0,le=50),user=Depends(volunteer),db:Session=Depends(get_db)):
    query=db.query(Need).filter_by(state=user.state,district=user.district,status=NeedStatus.reported)
    if lat is not None and lng is not None:
        point=func.ST_SetSRID(func.ST_MakePoint(lng,lat),4326)
        query=query.filter(func.ST_DWithin(cast(Need.location,Geography),cast(point,Geography),radius_km*1000))
    return [serialize(db,n) for n in query.order_by(Need.created_at).limit(100).all()]

def assigned(db,id,user,lock=False):
    statement=select(Need).where(Need.id==id,Need.state==user.state,Need.district==user.district)
    if lock:statement=statement.with_for_update()
    need=db.scalar(statement)
    if not need:raise HTTPException(404,"not_found")
    return need

@router.get("/tasks/{id}")
def detail(id:str,user=Depends(volunteer),db:Session=Depends(get_db)):
    return serialize(db,assigned(db,id,user),True)

class VerifyRequest(BaseModel):
    status:Literal["verified","rejected"]
    comments:str=Field(min_length=5,max_length=1000)

@router.patch("/tasks/{id}/verify")
def verify(id:str,data:VerifyRequest,user=Depends(volunteer),db:Session=Depends(get_db)):
    need=assigned(db,id,user,True)
    if need.reported_by_id==user.id:raise HTTPException(403,"independent_verification_required")
    if need.status!=NeedStatus.reported:raise HTTPException(409,"invalid_transition")
    need.status=NeedStatus(data.status);need.verified_by_id=user.id;need.verified_at=now();need.updated_at=now()
    db.add(NeedEvent(need_id=id,status=data.status))
    # Store review notes separately from public/owner-visible request history.
    from app.db.models.projects import ModerationNote
    db.add(ModerationNote(need_id=id,actor_id=user.id,note=data.comments))
    audit(db,user,"need."+data.status,id);db.commit()
    return serialize(db,need,True)

@router.post("/sync")
def sync(data:BatchNeeds,user=Depends(volunteer),db:Session=Depends(get_db)):
    needs=[create_need(db,item,user) for item in data.items]
    db.commit()
    return {"items":[{"client_id":n.client_id,"id":n.id} for n in needs]}
