from pydantic import BaseModel
from typing import Optional
from app.models.asset import SourceSystem

class AssetCreate(BaseModel):
    name: str
    type: str
    admin_unit_id: Optional[int] = None
    source_system: SourceSystem
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AssetResponse(BaseModel):
    id: int
    name: str
    type: str
    admin_unit_id: Optional[int] = None
    source_system: SourceSystem
    status: Optional[str] = None
    
    class Config:
        from_attributes = True
