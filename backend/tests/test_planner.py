from app.db.models.projects import PlanningContext
from app.db.models.needs import Need,NeedStatus
from app.db.models.users import now,uid

def test_planner_scope_and_formula(client,account,db):
    test_district="Test-"+uid()
    district,h=account("district_official",district=test_district)
    other,oh=account("district_official",district="OtherDistrict")
    db.add(PlanningContext(id=uid(),state="Odisha",district=test_district,locality="",ward_village="",category="water",
        latitude=20,longitude=85,infrastructure_stock=2,planned_investment=1,vulnerability=1.5,is_sample=True,source="synthetic_sample"))
    need=Need(id=uid(),category="water",description="Synthetic water test report",location="SRID=4326;POINT(85 20)",
        state="Odisha",district=test_district,locality="",ward_village="",status="verified",created_at=now())
    db.add(need);db.commit()
    r=client.get("/api/v1/planner/dashboard?district="+test_district,headers=h)
    assert r.status_code==200,r.text
    hotspot=r.json()["hotspots"][0]
    assert hotspot["gap_ratio"]==0.5
    assert "not an official government metric" in r.json()["label"]
    assert not client.get("/api/v1/planner/needs?district="+test_district,headers=oh).json()
    assert client.patch("/api/v1/planner/needs/"+need.id+"/status",headers=oh,json={"status":"planned"}).status_code==404
    assert client.patch("/api/v1/planner/needs/"+need.id+"/status",headers=h,json={"status":"resolved"}).status_code==409
    assert client.patch("/api/v1/planner/needs/"+need.id+"/status",headers=h,json={"status":"planned"}).status_code==200
    _,citizen=account()
    assert client.get("/api/v1/planner/dashboard",headers=citizen).status_code==403
