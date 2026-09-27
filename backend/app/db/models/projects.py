from sqlalchemy import Column,String,Float,Integer,DateTime,Boolean,ForeignKey,JSON
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
