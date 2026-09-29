"""Local assisted-report adapter; not connected to WhatsApp or a public webhook."""
import os
import uuid
from typing import Literal
import httpx
from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel,Field
app=FastAPI(title="JanVastu local channel adapter")
CORE_BACKEND_URL=os.environ.get("CORE_BACKEND_URL","http://127.0.0.1:8000/api/v1").rstrip("/")
class IncomingReport(BaseModel):
    description:str=Field(min_length=10,max_length=4000)
    latitude:float=Field(ge=-90,le=90)
    longitude:float=Field(ge=-180,le=180)
    state:str=Field(min_length=2)
    district:str=Field(min_length=2)
    consent:Literal[True]
    citizen_consent:Literal[True]
    client_id:str=Field(default_factory=lambda:str(uuid.uuid4()))
    language:Literal["en","hi","or"]="en"
@app.post("/webhook")
async def report(data:IncomingReport,authorization:str=Header(...)):
    async with httpx.AsyncClient(timeout=20) as client:
        headers={"Authorization":authorization}
        profile=await client.get(CORE_BACKEND_URL+"/auth/me",headers=headers)
        if profile.status_code!=200 or profile.json().get("role")!="volunteer":
            raise HTTPException(403,"Approved volunteer access required.")
        analysis=await client.post(CORE_BACKEND_URL+"/citizen/analyze",headers=headers,json={"description":data.description})
        if analysis.status_code!=200:raise HTTPException(502,"Analysis unavailable; retry later.")
        response=await client.post(CORE_BACKEND_URL+"/citizen/needs",headers=headers,json={**data.model_dump(),"category":analysis.json()["category"]})
        if response.status_code!=200:raise HTTPException(response.status_code,"Report could not be saved.")
        return {"tracking_id":response.json()["id"],"channel":"local_mock","provider_connected":False}
@app.get("/health")
def health():return {"status":"ok","provider_connected":False,"channel":"local_mock"}
