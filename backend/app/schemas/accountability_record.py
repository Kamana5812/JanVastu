from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.asset import AssetResponse

class AccountabilityRecordCreate(BaseModel):
    asset_id: int
    contractor_name: Optional[str] = None
    sanctioned_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    planned_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    responsible_official: Optional[str] = None
    department: Optional[str] = None

class AccountabilityRecordResponse(BaseModel):
    id: int
    asset_id: int
    contractor_name: Optional[str] = None
    sanctioned_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    planned_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    responsible_official: Optional[str] = None
    department: Optional[str] = None
    
    # We can include the nested asset details for the API response
    asset: Optional[AssetResponse] = None

    class Config:
        from_attributes = True
