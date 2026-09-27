from app.db.models.users import Consent
from tests.test_reporting import payload

def test_sync_verification_and_scope(client,account,db,monkeypatch):
    monkeypatch.setattr("app.routers.citizen.reverse",lambda *args:{"source":"user_provided","address":""})
    user,headers=account("volunteer")
    db.add(Consent(user_id=user.id,purpose="account_and_reporting"));db.commit()
    data=payload();data["citizen_consent"]=True
    first=client.post("/api/v1/volunteer/sync",headers=headers,json={"items":[data]})
    assert first.status_code==200,first.text
    id=first.json()["items"][0]["id"]
    assert client.post("/api/v1/volunteer/sync",headers=headers,json={"items":[data]}).json()["items"][0]["id"]==id
    assert client.patch(f"/api/v1/volunteer/tasks/{id}/verify",headers=headers,json={"status":"verified","comments":"Independent test review"}).status_code==403
    _,outside=account("volunteer",district="Cuttack")
    assert client.get(f"/api/v1/volunteer/tasks/{id}",headers=outside).status_code==404
    _,reviewer=account("volunteer")
    assert client.get(f"/api/v1/volunteer/tasks/{id}",headers=reviewer).json()["description"]==data["description"]
    assert client.patch(f"/api/v1/volunteer/tasks/{id}/verify",headers=reviewer,json={"status":"verified","comments":"Independent test review"}).status_code==200
    assert client.patch(f"/api/v1/volunteer/tasks/{id}/verify",headers=reviewer,json={"status":"verified","comments":"Repeated review"}).status_code==409
    _,citizen=account()
    assert client.get("/api/v1/volunteer/tasks",headers=citizen).status_code==403
    assert client.get("/api/v1/volunteer/stats",headers=reviewer).json()["verified_today"]>=1
