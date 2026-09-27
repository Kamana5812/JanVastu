from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AdminUnitBase(BaseModel):
    name: str
    type: str
    parent_id: Optional[int] = None

class AdminUnitCreate(AdminUnitBase):
    pass

class AdminUnitResponse(AdminUnitBase):
    id: int

    class Config:
        from_attributes = True
