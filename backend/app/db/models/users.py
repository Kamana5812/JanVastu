import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey, JSON
from app.db.base import Base

def uid():
    return str(uuid.uuid4())

def now():
    return datetime.now(timezone.utc)

class UserRole(str, enum.Enum):
    citizen = "citizen"
    volunteer = "volunteer"
    district_official = "district_official"
    state_planner = "state_planner"
    national_planner = "national_planner"
    auditor = "auditor"
    admin = "admin"

class UserStatus(str, enum.Enum):
    active = "active"
    pending_approval = "pending_approval"
    suspended = "suspended"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=uid)
    role = Column(Enum(UserRole), nullable=False)
    name = Column(String, nullable=False)
    mobile = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    preferred_language = Column(String, default="en", nullable=False)
    state = Column(String)
    district = Column(String)
    locality = Column(String)
    ward_village = Column(String)
    status = Column(Enum(UserStatus), default=UserStatus.pending_approval, nullable=False)
    token_version = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now)
    last_active = Column(DateTime(timezone=True))

class AccessRequest(Base):
    __tablename__ = "access_requests"
    id = Column(String, primary_key=True, default=uid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    role_requested = Column(String, nullable=False)
    organization = Column(String, default="")
    designation = Column(String, default="")
    reason = Column(String, default="")
    verification_info = Column(String, default="")
    status = Column(String, default="pending", nullable=False)
    reviewed_by = Column(String, ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=now)

class Consent(Base):
    __tablename__ = "consent_records"
    id = Column(String, primary_key=True, default=uid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    purpose = Column(String, nullable=False)
    language = Column(String, default="en")
    channel = Column(String, default="web")
    version = Column(String, default="2026-09-v1")
    status = Column(String, default="active")
    recorded_at = Column(DateTime(timezone=True), default=now)
    withdrawn_at = Column(DateTime(timezone=True))

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=uid)
    timestamp = Column(DateTime(timezone=True), default=now)
    actor_id = Column(String, nullable=True)
    role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    result = Column(String, default="success")

class AuthChallenge(Base):
    __tablename__ = "auth_challenges"
    id = Column(String, primary_key=True, default=uid)
    user_id = Column(String, ForeignKey("users.id"))
    purpose = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True))
    attempts = Column(Integer, default=0)

class RefreshSession(Base):
    __tablename__ = "refresh_sessions"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True))

class RateLimit(Base):
    __tablename__ = "rate_limits"
    key = Column(String, primary_key=True)
    count = Column(Integer, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
