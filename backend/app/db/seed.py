"""Idempotent synthetic planning/project seed. Never drops or resets tables."""
from datetime import datetime,timezone,timedelta
from app.db.base import SessionLocal
from app.db.models.projects import PlanningContext,Project,ProjectEvent
from app.db.models.users import now
from app.db.models.needs import Need,NeedEvent
from app.db.import_datasets import import_dataset
CATEGORIES=["water","sanitation","electricity","health","school","transport","road","housing","other"]
def seed_db():
    with SessionLocal() as db:
        areas=[("Puri",19.81,85.83),("Cuttack",20.46,85.88),("Khordha",20.30,85.82)]
        for i,(district,lat,lon) in enumerate(areas):
            for j,category in enumerate(CATEGORIES):
                id=f"sample-context-{i}-{j}"
                if not db.get(PlanningContext,id):
                    db.add(PlanningContext(id=id,state="Odisha",district=district,locality="Sample block",
                        ward_village="Sample ward",category=category,latitude=lat,longitude=lon,
                        infrastructure_stock=float(i+1),planned_investment=float(j%3),vulnerability=1+0.2*i,
                        source="synthetic_sample",is_sample=True))
        for i in range(6):
            id=f"SAMPLE-{i+1:03d}";district,lat,lon=areas[i%3]
            if db.get(Project,id):continue
            p=Project(id=id,name=f"Synthetic community project {i+1}",state="Odisha",district=district,
                locality="Sample block",ward_village="Sample ward",category=CATEGORIES[i],
                location=f"SRID=4326;POINT({lon+i*0.001} {lat+i*0.001})",
                department="Sample public works department",contractor=f"Synthetic contractor {i+1}",
                sanctioned_cost=1000000.0*(i+1),actual_cost=None if i%2==0 else 900000.0*(i+1),
                planned_start=datetime(2026,1,1,tzinfo=timezone.utc),
                planned_completion=datetime(2027,1,1,tzinfo=timezone.utc),
                actual_start=datetime(2026,2,1,tzinfo=timezone.utc),
                actual_completion=None if i<5 else datetime(2026,8,1,tzinfo=timezone.utc),
                responsible_agency="Sample civic agency",responsible_official="Sample engineering office",
                office_contact=None,department_chain="Sample ward / Sample district office",
                status="in_progress" if i<5 else "completed",progress=50 if i<5 else 100,is_sample=True,
                source_badges={k:"synthetic_sample" for k in ["identity","finance","schedule","responsibility"]})
            db.add(p);db.flush()
            stages=["sanctioned","tendered","awarded","started","in_progress"]+(["completed"] if i==5 else [])
            for j,stage in enumerate(stages):
                db.add(ProjectEvent(project_id=id,stage=stage,occurred_at=datetime(2026,1,1,tzinfo=timezone.utc)+timedelta(days=30*j)))
        for i,(district,lat,lon) in enumerate(areas):
            for j,category in enumerate(CATEGORIES):
                nid=f"sample-need-{i}-{j}"
                if not db.get(Need,nid):
                    status=["reported","verified","planned"][j%3]
                    db.add(Need(id=nid,category=category,description=f"Synthetic demonstration request for {category}. No real citizen submitted this record.",
                        location=f"SRID=4326;POINT({lon} {lat})",state="Odisha",district=district,locality="Sample block",ward_village="Sample ward",
                        status=status,is_sample=True,created_at=now()-timedelta(days=j),language="en"))
                    db.flush();db.add(NeedEvent(need_id=nid,status=status))
        for project in db.query(Project).filter_by(is_sample=True):
            project.source_badges={key:"Synthetic Sample" if getattr(project,key) is not None and getattr(project,key)!="" else "Information Not Available" for key in ("name","category","state","district","locality","ward_village","department","contractor","sanctioned_cost","actual_cost","planned_start","planned_completion","actual_start","actual_completion","responsible_agency","responsible_official","office_contact","department_chain","status","progress")}
            project.source_badges={**project.source_badges,"timeline":"Synthetic Sample"}
        imported=import_dataset(db)
        db.commit()
        print(f"Imported {imported} supplied infrastructure records with provenance.")
        print("Synthetic planning contexts and six sample projects are ready. Existing records preserved.")
if __name__=="__main__":seed_db()
