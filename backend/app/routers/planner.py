from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List

from app.db.base import get_db
from app.db.models.users import User, UserRole
from app.db.models.needs import Need, NeedStatus
from app.core.rbac import require_role

router = APIRouter()

class StatusUpdateRequest(BaseModel):
    status: NeedStatus

@router.get("/stats")
def get_planner_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.district_official, UserRole.state_planner, UserRole.national_planner]))
):
    query = db.query(Need.status, func.count(Need.id)).group_by(Need.status)
    
    # Filter based on planner scope (using their location metadata which would be in a real app)
    # For hackathon, we assume they can see aggregated stats for their jurisdiction
    
    results = query.all()
    stats = {status.value: count for status, count in results}
    
    return {
        "total": sum(stats.values()),
        "by_status": stats
    }

@router.get("/needs")
def get_planner_needs(
    status: NeedStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.district_official, UserRole.state_planner, UserRole.national_planner]))
):
    query = db.query(Need)
    if status:
        query = query.filter(Need.status == status)
        
    # Would apply geographic filtering here based on user role (e.g. National sees all, District sees only their district)
    
    needs = query.order_by(Need.created_at.desc()).limit(100).all()
    
    return [{
        "id": n.id,
        "category": n.category,
        "description": n.description,
        "status": n.status,
        "district": n.district,
        "state": n.state,
        "affected_people": n.affected_people,
        "created_at": n.created_at
    } for n in needs]

@router.patch("/needs/{need_id}/status")
def update_need_status(
    need_id: str,
    data: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.district_official, UserRole.state_planner, UserRole.national_planner]))
):
    need = db.query(Need).filter(Need.id == need_id).first()
    if not need:
        raise HTTPException(status_code=404, detail="Need not found")
        
    # Planners can change verified to planned/resolved
    need.status = data.status
    db.commit()
    
    return {"message": "Status updated", "status": need.status}
