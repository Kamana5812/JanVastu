from app.db.models.users import uid
def test_mobile_registration(client):
    mobile="9"+str(int(uid().replace("-","")[:12],16))[:9]
    r=client.post("/api/v1/auth/signup/otp/request",json={"name":"Synthetic OTP citizen","mobile":mobile,"state":"Odisha","district":"Puri","consent":True})
    assert r.status_code==200,r.text
    challenge=r.json()["challenge_id"]
    assert client.post("/api/v1/auth/signup/otp/verify",json={"challenge_id":challenge,"code":"111111"}).status_code==400
    result=client.post("/api/v1/auth/signup/otp/verify",json={"challenge_id":challenge,"code":"123456"})
    assert result.status_code==200,result.text
    assert result.json()["user"]["role"]=="citizen"
    assert client.post("/api/v1/auth/signup/otp/verify",json={"challenge_id":challenge,"code":"123456"}).status_code==400
def test_google_validation_and_replay(client,account,monkeypatch):
    from app.core.config import settings
    user,_=account()
    monkeypatch.setattr(settings,"GOOGLE_CLIENT_ID","test-client")
    r=client.post("/api/v1/auth/google/challenge");nonce=r.json()["nonce"]
    monkeypatch.setattr("app.services.google_identity.verify",lambda token:{"email":user.email,"nonce":"wrong"})
    data={"nonce":nonce,"credential":"synthetic-token-value-123"}
    assert client.post("/api/v1/auth/google",json=data).status_code==401
    monkeypatch.setattr("app.services.google_identity.verify",lambda token:{"email":user.email,"nonce":nonce})
    assert client.post("/api/v1/auth/google",json=data).status_code==200
    assert client.post("/api/v1/auth/google",json=data).status_code==401
def test_every_role_access_matrix(client,account):
    reporters={"citizen","volunteer"};planners={"district_official","state_planner","national_planner"}
    for role in ["citizen","volunteer","district_official","state_planner","national_planner","admin","auditor"]:
        _,h=account(role)
        for path,allowed in [("/citizen/needs",reporters),("/volunteer/tasks",{"volunteer"}),("/planner/dashboard",planners),("/admin/users",{"admin"}),("/ai-ops/pipelines",{"admin","auditor"}),("/admin/audit-logs",{"admin","auditor"})]:
            r=client.get("/api/v1"+path,headers=h)
            assert r.status_code==(200 if role in allowed else 403),(role,path,r.text)
