from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.base import get_db
from app.db.models.users import User, UserRole, UserStatus
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user(token=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    try:
        payload = decode_token(token or "", "access")
        user = db.get(User, payload.get("sub"))
        if not user or user.status != UserStatus.active or payload.get("ver") != user.token_version:
            raise ValueError("Inactive session")
        return user
    except (JWTError, ValueError, TypeError, AttributeError):
        raise HTTPException(401, "session_expired", headers={"WWW-Authenticate": "Bearer"})

def require_role(roles):
    def check(user: User=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "access_denied")
        return user
    return check

PLANNERS = [UserRole.district_official, UserRole.state_planner, UserRole.national_planner]
GOVERNANCE = [UserRole.admin, UserRole.auditor]

def scoped(query, model, user):
    if user.role == UserRole.district_official:
        return query.filter(model.state == user.state, model.district == user.district)
    if user.role == UserRole.state_planner:
        return query.filter(model.state == user.state)
    return query

def in_scope(item, user):
    if user.role == UserRole.district_official:
        return item.state == user.state and item.district == user.district
    if user.role == UserRole.state_planner:
        return item.state == user.state
    return user.role in [UserRole.national_planner, UserRole.admin]
