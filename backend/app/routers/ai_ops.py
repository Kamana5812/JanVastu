from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.base import get_db
from app.db.models.needs import PipelineRun,Need
from app.core.rbac import require_role,GOVERNANCE

router=APIRouter()
@router.get("/metrics")
@router.get("/pipelines")
def metrics(user=Depends(require_role(GOVERNANCE)),db:Session=Depends(get_db)):
    rows=db.query(PipelineRun.stage,PipelineRun.model_version,func.count(PipelineRun.id),func.avg(PipelineRun.latency_ms)).group_by(PipelineRun.stage,PipelineRun.model_version).all()
    stages=[]
    for stage,version,count,latency in rows:
        failures=db.query(PipelineRun).filter_by(stage=stage,model_version=version,success=False).count()
        stages.append({"stage":stage,"version":version,"processed":count,"failed":failures,"average_latency_ms":round(latency,2),"accuracy":None})
    def distribution(column):
        return [{"label":label or "unknown","count":count} for label,count in db.query(column,func.count(PipelineRun.id)).filter(column.isnot(None)).group_by(column)]
    return {"pipelines":stages,"languages":distribution(PipelineRun.language),"categories":distribution(PipelineRun.category),
        "total_runs":db.query(PipelineRun).count(),"review_required":db.query(Need).filter(Need.moderation_reason.isnot(None)).count(),
        "planned":["speech_transcription","translation","image_anonymization"],
        "scope":"Lightweight language detection, keyword classification and geocoding. Accuracy has not been evaluated."}
