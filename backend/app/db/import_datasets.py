"""Idempotent import of supplied observations; never update curated project fields."""
import json
from pathlib import Path
from app.db.base import SessionLocal
from app.db.models.projects import Project

DATA_PATH=Path(__file__).resolve().parents[1]/"data"/"bhubaneswar.json"
BADGE="User supplied — unverified"

def import_dataset(db):
    data=json.loads(DATA_PATH.read_text(encoding="utf-8"))
    inserted=0
    for asset in data["assets"]:
        if db.get(Project,asset["id"]):continue
        sources={sid:source for sid,source in data["sources"].items() if any(sid in claim["sources"] for claim in asset["claims"])}
        record={**asset,"sources":sources,"imported_on":data["imported_on"]}
        db.add(Project(id=asset["id"],name=asset["name"],state="Odisha",district="",category=asset["category"],
            location=None,status="unverified",progress=None,is_sample=False,dataset_record=record,
            source_badges={key:BADGE for key in ("name","state","category")}))
        inserted+=1
    db.flush()
    return inserted

if __name__=="__main__":
    with SessionLocal() as db:
        count=import_dataset(db)
        db.commit()
        print(f"Imported {count} supplied infrastructure records; existing records preserved.")
