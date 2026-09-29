from sqlalchemy import text
from app.db.models.users import Consent,uid
from app.db.models.projects import Project,ProjectEvent
from app.db.models.needs import Need
from app.db.models.users import now

def test_public_project_sources(client,db):
    p=Project(id=uid(),name="Synthetic test project",state="Odisha",district="Puri",category="water",
        location="SRID=4326;POINT(85 20)",status="planned",progress=0,is_sample=True,source_badges={"name":"Synthetic Sample"})
    db.add(p);db.commit()
    result=client.get("/api/v1/projects/"+p.id)
    assert result.status_code==200
    fields=result.json()["fields"]
    assert fields["name"]["source_badge"]=="Synthetic Sample"
    assert fields["actual_cost"]=={"value":None,"source_badge":"Information Not Available"}
    assert client.get("/api/v1/projects/search?q=Synthetic").status_code==200
    assert client.get("/api/v1/projects/search?lat=20").status_code==422
    assert "reported_by_id" not in result.text

def test_consent_and_audit_roles(client,account,db):
    user,h=account();other,oh=account();admin,ah=account("admin");auditor,audh=account("auditor")
    c=Consent(user_id=user.id,purpose="account_and_reporting");db.add(c);db.commit()
    assert client.patch("/api/v1/account/consents/"+c.id,headers=oh,json={"status":"withdrawn"}).status_code==404
    assert client.patch("/api/v1/account/consents/"+c.id,headers=h,json={"status":"withdrawn"}).status_code==200
    assert client.get("/api/v1/account/consents",headers=h).json()[0]["status"]=="withdrawn"
    assert client.patch("/api/v1/admin/consent/"+c.id,headers=ah,json={"status":"active"}).status_code==422
    for path in ["/admin/overview","/admin/roles","/admin/requests","/admin/consent","/admin/integrations","/admin/reports","/admin/data-governance"]:
        assert client.get("/api/v1"+path,headers=h).status_code==403
        response=client.get("/api/v1"+path,headers=ah)
        assert response.status_code==200,response.text
    assert client.get("/api/v1/admin/audit-logs",headers=audh).status_code==200
    assert client.get("/api/v1/ai-ops/pipelines",headers=audh).status_code==200
    assert client.get("/api/v1/ai-ops/pipelines",headers=h).status_code==403
    assert client.patch("/api/v1/admin/audit-logs/x",headers=ah,json={"result":"changed"}).status_code in (404,405)
    assert all(i["status"] in ("planned","not_connected") for i in client.get("/api/v1/admin/integrations",headers=ah).json())

def test_moderation(client,account,db):
    _,h=account("admin")
    n=Need(id=uid(),category="water",description="Synthetic review case",location="SRID=4326;POINT(85 20)",
        state="Odisha",district="Puri",status="reported",moderation_reason="duplicate")
    db.add(n);db.commit()
    r=client.patch("/api/v1/admin/requests/"+n.id,headers=h,json={"action":"reject","note":"Synthetic review reason"})
    assert r.status_code==200,r.text
    assert r.json()["status"]=="rejected"
    assert "Synthetic review reason" not in client.get("/api/v1/admin/requests",headers=h).text

def test_runtime_audit_privileges(db):
    for privilege in ("UPDATE","DELETE","TRUNCATE"):
        assert not db.scalar(text("SELECT has_table_privilege('janvastu_api','audit_logs',:privilege)"),{"privilege":privilege})
    assert db.scalar(text("SELECT has_table_privilege('janvastu_api','audit_logs','INSERT')"))
