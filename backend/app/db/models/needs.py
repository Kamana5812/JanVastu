import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, Float, Boolean, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.base import Base
from app.db.models.users import uid, now

class NeedCategory(str, enum.Enum):
    water="water"
    road="road"
    health="health"
    school="school"
    electricity="electricity"
    sanitation="sanitation"
    transport="transport"
    housing="housing"
    other="other"

class NeedStatus(str, enum.Enum):
    reported="reported"
    verified="verified"
    planned="planned"
    resolved="resolved"
    rejected="rejected"

class Need(Base):
    __tablename__="needs"
    __table_args__=(UniqueConstraint("reported_by_id","client_id",name="uq_need_client"),)
    id=Column(String,primary_key=True,default=uid)
    category=Column(Enum(NeedCategory),nullable=False)
    description=Column(String,nullable=False)
    is_sample=Column(Boolean,nullable=False,default=False)
    affected_people=Column(Integer)
    location=Column(Geometry("POINT",srid=4326),nullable=False)
    address=Column(String)
    state=Column(String,nullable=False)
    district=Column(String,nullable=False)
    locality=Column(String,default="")
    ward_village=Column(String,default="")
    status=Column(Enum(NeedStatus),default=NeedStatus.reported,nullable=False)
    reported_by_id=Column(String,ForeignKey("users.id"))
    consent_id=Column(String,ForeignKey("consent_records.id"))
    project_id=Column(String)
    client_id=Column(String)
    payload_hash=Column(String)
    language=Column(String,default="en")
    geocoding_source=Column(String,default="user_provided")
    moderation_reason=Column(String)
    created_at=Column(DateTime(timezone=True),default=now)
    updated_at=Column(DateTime(timezone=True),default=now)
    verified_by_id=Column(String,ForeignKey("users.id"))
    verified_at=Column(DateTime(timezone=True))
    evidence=relationship("Evidence",back_populates="need")
    events=relationship("NeedEvent",order_by="NeedEvent.created_at")

class Evidence(Base):
    __tablename__="evidence"
    id=Column(String,primary_key=True,default=uid)
    need_id=Column(String,ForeignKey("needs.id"),nullable=False)
    file_url=Column(String,nullable=False)
    uploaded_by_id=Column(String,ForeignKey("users.id"))
    created_at=Column(DateTime(timezone=True),default=now)
    content_type=Column(String)
    size_bytes=Column(Integer)
    anonymized=Column(Boolean,default=False,nullable=False)
    public_file_url=Column(String)
    need=relationship("Need",back_populates="evidence")

class NeedEvent(Base):
    __tablename__="need_events"
    id=Column(String,primary_key=True,default=uid)
    need_id=Column(String,ForeignKey("needs.id"),nullable=False)
    status=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),default=now)

class PipelineRun(Base):
    __tablename__="pipeline_runs"
    id=Column(String,primary_key=True,default=uid)
    need_id=Column(String,ForeignKey("needs.id"))
    stage=Column(String,nullable=False)
    model_version=Column(String,nullable=False)
    latency_ms=Column(Float,nullable=False)
    success=Column(Boolean,nullable=False)
    language=Column(String)
    category=Column(String)
    confidence=Column(Float)
    created_at=Column(DateTime(timezone=True),default=now)
