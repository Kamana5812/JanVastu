from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConsentCreate(BaseModel):
    purpose: str
    language: str
    channel: str

class ConsentResponse(BaseModel):
    id: str
    purpose: str
    language: str
    channel: str
    timestamp: datetime
    consent_hash: str

    class Config:
        from_attributes = True
