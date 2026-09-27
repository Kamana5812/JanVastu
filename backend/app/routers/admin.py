from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Literal
from app.db.base import get_db
from app.db.models.users import User, UserRole, UserStatus, AccessRequest, now
from app.schemas.auth import LoginRequest
from app.core.rbac import require_role
from app.routers.auth import limit, password_login
from app.services.audit import audit

router = APIRouter()
admin = require_role([UserRole.admin])

@router.post("/login")
def login(data: LoginRequest, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "admin_login")
    return password_login(data, db, admin_only=True)

@router.get("/users")
def users(status: UserStatus | None=None, user=Depends(admin), db: Session=Depends(get_db)):
    query = db.query(User)
    if status:
        query = query.filter(User.status == status)
    return [{"id": u.id, "name": u.name, "role": u.role, "status": u.status,
             "state": u.state, "district": u.district, "last_active": u.last_active,
             "created_at": u.created_at} for u in query.order_by(User.created_at.desc()).all()]

class StatusUpdate(BaseModel):
    status: Literal["active", "suspended", "rejected"]

@router.patch("/users/{user_id}/status")
def update(user_id: str, data: StatusUpdate, user=Depends(admin), db: Session=Depends(get_db)):
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404, "not_found")
    if target.id == user.id or target.role == UserRole.admin:
        raise HTTPException(400, "admin_status_protected")
    target.status = UserStatus(data.status)
    target.token_version += 1
    application = db.query(AccessRequest).filter_by(user_id=target.id).first()
    if application and application.status == "pending":
        if data.status not in ("active", "rejected"):
            raise HTTPException(400, "invalid_transition")
        application.status = "approved" if data.status == "active" else "rejected"
        application.reviewed_by = user.id
        application.reviewed_at = now()
    audit(db, user, "user.status."+data.status, target.id)
    db.commit()
    return {"status": target.status}

@router.get("/access-requests")
def applications(user=Depends(admin), db: Session=Depends(get_db)):
    return [{"id": a.id, "user_id": a.user_id, "name": u.name,
             "role_requested": a.role_requested, "organization": a.organization,
             "designation": a.designation, "reason": a.reason,
             "verification_info": a.verification_info, "state": u.state,
             "district": u.district, "status": a.status, "created_at": a.created_at}
            for a, u in db.query(AccessRequest, User).join(User, AccessRequest.user_id == User.id).all()]
