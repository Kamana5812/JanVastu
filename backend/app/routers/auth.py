from datetime import timedelta
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.base import get_db
from app.db.models.users import User, UserRole, UserStatus, AccessRequest, Consent, AuthChallenge, RefreshSession, RateLimit, now, uid
from app.schemas.auth import Signup, AccessRequestCreate, LoginRequest, OTPVerify, ResetRequest, ResetConfirm, RefreshRequest, ProfileUpdate
from app.core.security import get_password_hash, verify_password, create_token, decode_token
from app.core.rbac import get_current_user
from app.core.config import settings
from app.services.audit import audit

router = APIRouter()

def profile(user):
    return {key: getattr(user, key) for key in ("id", "name", "email", "mobile", "role", "status", "preferred_language", "state", "district", "locality", "ward_village")}

def limit(db, request, action):
    key = hashlib.sha256(f"{request.client.host if request.client else 'test'}:{action}".encode()).hexdigest()
    # PostgreSQL advisory lock serializes increments across API workers.
    db.execute(__import__('sqlalchemy').text("SELECT pg_advisory_xact_lock(:key)"), {"key": int(key[:15], 16)})
    row = db.get(RateLimit, key)
    if not row:
        row = RateLimit(key=key, count=0, expires_at=now()+timedelta(minutes=15))
        db.add(row)
    if row.expires_at <= now():
        row.count = 0
        row.expires_at = now()+timedelta(minutes=15)
    if row.count >= 30:
        db.rollback()
        raise HTTPException(429, "too_many_attempts", headers={"Retry-After": "900"})
    row.count += 1
    db.commit()

def tokens(db, user):
    session = RefreshSession(id=uid(), user_id=user.id, expires_at=now()+timedelta(days=7))
    db.add(session)
    user.last_active = now()
    audit(db, user, "session.created", session.id)
    db.commit()
    return {"access_token": create_token(user), "refresh_token": create_token(user, "refresh", 10080, session.id), "user": profile(user), "token_type": "bearer"}

def challenge(db, user, purpose):
    if not settings.MOCK_OTP_ENABLED:
        raise HTTPException(503, "otp_delivery_not_configured")
    row = AuthChallenge(user_id=user.id if user else None, purpose=purpose, expires_at=now()+timedelta(minutes=5))
    db.add(row)
    db.commit()
    return {"challenge_id": row.id, "requires_otp": True, "mode": "demo", "expires_in": 300}

def verify_challenge(db, data, purpose):
    row = db.scalar(select(AuthChallenge).where(AuthChallenge.id == data.challenge_id).with_for_update())
    if not settings.MOCK_OTP_ENABLED or not row or row.purpose != purpose or row.used_at or row.expires_at <= now() or row.attempts >= 5:
        raise HTTPException(400, "invalid_challenge")
    row.attempts += 1
    if data.code != "123456":
        db.commit()
        raise HTTPException(400, "invalid_otp")
    row.used_at = now()
    user = db.get(User, row.user_id) if row.user_id else None
    db.commit()
    if not user or user.status != UserStatus.active:
        raise HTTPException(400, "invalid_challenge")
    return user

def register(data, role, db):
    email = str(data.email).lower() if data.email else None
    clauses = []
    if email:
        clauses.append(User.email == email)
    if data.mobile:
        clauses.append(User.mobile == data.mobile)
    if db.query(User).filter(or_(*clauses)).first():
        raise HTTPException(409, "account_exists")
    user = User(name=data.name.strip(), email=email, mobile=data.mobile, role=role,
        password_hash=get_password_hash(data.password), preferred_language=data.preferred_language,
        state=data.state.strip(), district=data.district.strip(), locality=data.locality,
        ward_village=data.ward_village, status=UserStatus.active if role == UserRole.citizen else UserStatus.pending_approval)
    db.add(user)
    db.flush()
    db.add(Consent(user_id=user.id, purpose="account_and_reporting", language=data.preferred_language))
    if role != UserRole.citizen:
        db.add(AccessRequest(user_id=user.id, role_requested=role.value,
            organization=getattr(data, "organization", data.area), designation=getattr(data, "designation", ""),
            reason=getattr(data, "reason", data.experience), verification_info=getattr(data, "verification_info", "")))
    audit(db, user, "account.registered", user.id)
    db.commit()
    return user

@router.get("/options")
def options():
    return {"demo_otp": settings.MOCK_OTP_ENABLED, "google_available": False}

@router.post("/signup/citizen")
def citizen(data: Signup, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "signup")
    return tokens(db, register(data, UserRole.citizen, db))

@router.post("/signup/volunteer")
def volunteer(data: Signup, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "signup")
    register(data, UserRole.volunteer, db)
    return {"message": "application_submitted"}

@router.post("/access-request")
def access(data: AccessRequestCreate, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "signup")
    register(data, UserRole(data.role_requested), db)
    return {"message": "application_submitted"}

def password_login(data, db, admin_only=False):
    user = db.query(User).filter(or_(User.email == data.identifier.lower(), User.mobile == data.identifier)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "invalid_credentials")
    if admin_only and user.role != UserRole.admin:
        raise HTTPException(403, "access_denied")
    if user.status != UserStatus.active:
        raise HTTPException(403, "account_not_active")
    if user.role in (UserRole.admin, UserRole.auditor, UserRole.district_official, UserRole.state_planner, UserRole.national_planner):
        return challenge(db, user, "login")
    return tokens(db, user)

@router.post("/login")
def login(data: LoginRequest, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "login")
    return password_login(data, db)

@router.post("/otp/request")
def request_otp(data: ResetRequest, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "otp")
    user = db.query(User).filter(or_(User.email == data.identifier.lower(), User.mobile == data.identifier)).first()
    return challenge(db, user if user and user.status == UserStatus.active else None, "login")

@router.post("/otp/verify")
def otp(data: OTPVerify, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "otp_verify")
    return tokens(db, verify_challenge(db, data, "login"))

@router.post("/password/reset-request")
def reset_request(data: ResetRequest, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "reset")
    user = db.query(User).filter(or_(User.email == data.identifier.lower(), User.mobile == data.identifier)).first()
    return challenge(db, user, "reset")

@router.post("/password/reset")
def reset(data: ResetConfirm, request: Request, db: Session=Depends(get_db)):
    limit(db, request, "reset_confirm")
    user = verify_challenge(db, data, "reset")
    user.password_hash = get_password_hash(data.password)
    user.token_version += 1
    audit(db, user, "password.reset", user.id)
    db.commit()
    return {"message": "password_updated"}

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session=Depends(get_db)):
    try:
        p = decode_token(data.refresh_token, "refresh")
        session = db.scalar(select(RefreshSession).where(RefreshSession.id == p["jti"]).with_for_update())
        user = db.get(User, p["sub"])
        if not session or session.revoked_at or session.expires_at <= now() or session.user_id != p["sub"] or not user or user.status != UserStatus.active or p.get("ver") != user.token_version:
            raise ValueError()
        session.revoked_at = now()
        return tokens(db, user)
    except (JWTError, ValueError, KeyError):
        raise HTTPException(401, "session_expired")

@router.post("/logout")
def logout(user=Depends(get_current_user), db: Session=Depends(get_db)):
    user.token_version += 1
    audit(db, user, "session.logout", user.id)
    db.commit()
    return {"message": "signed_out"}

@router.get("/me")
def me(user=Depends(get_current_user)):
    return profile(user)

@router.patch("/me")
def edit_me(data: ProfileUpdate, user=Depends(get_current_user), db: Session=Depends(get_db)):
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    audit(db, user, "profile.updated", user.id)
    db.commit()
    return profile(user)
