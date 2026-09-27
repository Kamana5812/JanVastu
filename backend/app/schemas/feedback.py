from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.feedback import FeedbackCategory, FeedbackStatus

class FeedbackCreate(BaseModel):
    consent_id: str
    category: Optional[FeedbackCategory] = None
    description_text: Optional[str] = None
    language: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    media_urls: Optional[List[str]] = None

class FeedbackResponse(BaseModel):
    id: int
    consent_id: str
    category: Optional[FeedbackCategory] = None
    description_text: Optional[str] = None
    language: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    admin_unit_id: Optional[int] = None
    status: FeedbackStatus
    media_urls: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeedbackEnrich(BaseModel):
    category: Optional[FeedbackCategory] = None
    language: Optional[str] = None

class FeedbackUpdate(BaseModel):
    status: Optional[FeedbackStatus] = None
