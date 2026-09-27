from typing import Literal
from pydantic import BaseModel, Field
from app.db.models.needs import NeedCategory

class NeedCreate(BaseModel):
    category: NeedCategory
    description: str=Field(min_length=10,max_length=4000)
    affected_people: int | None=Field(default=None,ge=1,le=10000000)
    latitude: float=Field(ge=-90,le=90)
    longitude: float=Field(ge=-180,le=180)
    address: str=Field(default="",max_length=500)
    state: str=Field(min_length=2,max_length=100)
    district: str=Field(min_length=2,max_length=100)
    locality: str=Field(default="",max_length=150)
    ward_village: str=Field(default="",max_length=150)
    client_id: str=Field(min_length=8,max_length=80)
    project_id: str | None=None
    consent: Literal[True]
    language: Literal["en","hi","or"]="en"
    citizen_consent: bool=False

class AnalyzeRequest(BaseModel):
    description: str=Field(min_length=10,max_length=4000)

class BatchNeeds(BaseModel):
    items: list[NeedCreate]=Field(min_length=1,max_length=50)
