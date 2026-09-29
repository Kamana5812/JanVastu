from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import Literal
from datetime import timedelta
from app.db.base import get_db
from app.db.models.needs import Need,NeedStatus,NeedEvent
from app.db.models.users import now
from app.core.rbac import require_role,PLANNERS,scoped,in_scope
from app.services.decision_service import dashboard,filtered
from app.services.audit import audit
router=APIRouter()
official=require_role(PLANNERS)

@router.get("/dashboard")
def get_dashboard(state:str="",district:str="",locality:str="",ward_village:str="",category:str="",
    project_status:str="",days:int=Query(default=90,ge=1,le=90),user=Depends(official),db:Session=Depends(get_db)):
    return dashboard(db,user,locals(),days)

@router.get("/needs")
def get_needs(status:NeedStatus|None=None,state:str="",district:str="",locality:str="",ward_village:str="",category:str="",
    days:int=Query(default=90,ge=1,le=90),user=Depends(official),db:Session=Depends(get_db)):
    query=filtered(scoped(db.query(Need),Need,user),Need,locals())
    query=query.filter(Need.created_at>=now()-timedelta(days=days))
    if status:query=query.filter(Need.status==status)
    return [{k:getattr(n,k) for k in ("id","is_sample","category","description","status","state","district","locality","ward_village","affected_people","created_at")}
        for n in query.order_by(Need.created_at.desc()).limit(500).all()]

@router.get("/stats")
def stats(user=Depends(official),db:Session=Depends(get_db)):
    d=dashboard(db,user,{})
    return {"total":d["kpis"]["total"],"by_status":d["by_status"]}

class Update(BaseModel):
    status:Literal["planned","resolved"]

@router.patch("/needs/{id}/status")
def update(id:str,data:Update,user=Depends(official),db:Session=Depends(get_db)):
    n=db.scalar(select(Need).where(Need.id==id).with_for_update())
    if not n or not in_scope(n,user):raise HTTPException(404,"not_found")
    if (n.status.value,data.status) not in (("verified","planned"),("planned","resolved")):
        raise HTTPException(409,"invalid_transition")
    n.status=NeedStatus(data.status);n.updated_at=now()
    db.add(NeedEvent(need_id=id,status=data.status))
    audit(db,user,"need."+data.status,id);db.commit()
    return {"status":n.status}
