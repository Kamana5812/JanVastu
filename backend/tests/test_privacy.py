from io import BytesIO
from PIL import Image
from app.db.models.users import Consent,uid
from app.db.models.needs import Need,Evidence
from app.db.models.projects import Project
def test_public_derivative_needs_review_and_active_consent(client,account,db,monkeypatch):
    user,h=account();_,admin=account("admin")
    account_consent=Consent(user_id=user.id,purpose="account_and_reporting")
    report_consent=Consent(user_id=user.id,purpose="report")
    db.add_all([account_consent,report_consent]);db.flush()
    p=Project(id=uid(),name="Synthetic privacy project",state="Odisha",district="Puri",category="water",
        location="SRID=4326;POINT(85 20)",status="planned",progress=0,is_sample=True,source_badges={"name":"Synthetic Sample"})
    db.add(p);db.flush()
    n=Need(id=uid(),description="Synthetic privacy report",category="water",state="Odisha",district="Puri",
        location="SRID=4326;POINT(85 20)",project_id=p.id,reported_by_id=user.id,consent_id=report_consent.id)
    db.add(n);db.flush()
    e=Evidence(need_id=n.id,file_url="private/original.jpg",uploaded_by_id=user.id,content_type="image/jpeg")
    db.add(e);db.commit()
    assert not client.get("/api/v1/projects/"+p.id).json()["evidence"]
    assert client.get("/api/v1/projects/evidence/"+e.id+"/media").status_code==404
    raw=BytesIO();Image.new("RGB",(8,8),"blue").save(raw,format="JPEG")
    uploads=[];monkeypatch.setattr("app.routers.governance.put_media",lambda *args:uploads.append(args))
    response=client.post("/api/v1/admin/evidence/"+e.id+"/publish",headers=admin,data={"reviewed":"true"},
        files={"file":("redacted.jpg",raw.getvalue(),"image/jpeg")})
    assert response.status_code==200,response.text
    assert uploads[0][0].startswith("public-evidence/")
    db.refresh(e);assert e.file_url=="private/original.jpg"
    assert len(client.get("/api/v1/projects/"+p.id).json()["evidence"])==1
    client.patch("/api/v1/account/consents/"+account_consent.id,headers=h,json={"status":"withdrawn"})
    assert not client.get("/api/v1/projects/"+p.id).json()["evidence"]
    assert client.get("/api/v1/projects/evidence/"+e.id+"/media").status_code==404
def test_erasure_requires_password_and_revokes_session(client,account,db):
    user,h=account()
    assert client.post("/api/v1/account/erase",headers=h,json={"password":"wrong-password","confirm":True}).status_code==401
    assert client.post("/api/v1/account/erase",headers=h,json={"password":"Test-password-27","confirm":True}).status_code==200
    db.refresh(user);assert user.email is None and user.mobile is None and user.name=="[erased]"
    assert client.get("/api/v1/auth/me",headers=h).status_code==401
