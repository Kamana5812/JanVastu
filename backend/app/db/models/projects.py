from sqlalchemy import Column,String,Float,Integer,DateTime,Boolean,ForeignKey,JSON,UniqueConstraint,CheckConstraint
from geoalchemy2 import Geometry
from app.db.base import Base
from app.db.models.users import uid,now

class ModerationNote(Base):
    __tablename__="moderation_notes"
    id=Column(String,primary_key=True,default=uid)
    need_id=Column(String,ForeignKey("needs.id"),nullable=False)
    actor_id=Column(String,ForeignKey("users.id"),nullable=False)
    note=Column(String,nullable=False)
    created_at=Column(DateTime(timezone=True),default=now)

class PlanningContext(Base):
    __tablename__="planning_context"
    __table_args__=(UniqueConstraint("state","district","locality","ward_village","category",name="uq_planning_area"),)
    id=Column(String,primary_key=True,default=uid)
    state=Column(String,nullable=False)
    district=Column(String,nullable=False)
    locality=Column(String,default="",nullable=False)
    ward_village=Column(String,default="",nullable=False)
    category=Column(String,nullable=False)
    latitude=Column(Float,nullable=False)
    longitude=Column(Float,nullable=False)
    infrastructure_stock=Column(Float,nullable=False)
    planned_investment=Column(Float,nullable=False)
    vulnerability=Column(Float,nullable=False)
    source=Column(String,nullable=False,default="synthetic_sample")
    is_sample=Column(Boolean,nullable=False,default=True)

class Project(Base):
    __tablename__="projects"
    id=Column(String,primary_key=True,default=uid)
    name=Column(String,nullable=False)
    state=Column(String,nullable=False)
    district=Column(String,nullable=False)
    locality=Column(String,default="")
    ward_village=Column(String,default="")
    category=Column(String,nullable=False)
    location=Column(Geometry("POINT",srid=4326),nullable=True)
    department=Column(String)
    contractor=Column(String)
    sanctioned_cost=Column(Float)
    actual_cost=Column(Float)
    planned_start=Column(DateTime(timezone=True))
    planned_completion=Column(DateTime(timezone=True))
    actual_start=Column(DateTime(timezone=True))
    actual_completion=Column(DateTime(timezone=True))
    responsible_agency=Column(String)
    responsible_official=Column(String)
    office_contact=Column(String)
    department_chain=Column(String)
    status=Column(String,nullable=False)
    progress=Column(Integer,nullable=True)
    dataset_record=Column(JSON,nullable=True)
    source_badges=Column(JSON,nullable=False,default=dict)
    is_sample=Column(Boolean,nullable=False,default=True)

class ProjectEvent(Base):
    __tablename__="project_timeline_events"
    id=Column(String,primary_key=True,default=uid)
    project_id=Column(String,ForeignKey("projects.id"),nullable=False)
    stage=Column(String,nullable=False)
    occurred_at=Column(DateTime(timezone=True),nullable=False)

class IntegrationStatus(Base):
    __tablename__="integrations_status"
    __table_args__=(CheckConstraint("status IN ('not_connected','planned')",name="integration_honesty"),)
    name=Column(String,primary_key=True)
    status=Column(String,nullable=False,default="planned")
