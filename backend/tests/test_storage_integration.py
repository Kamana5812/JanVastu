import os
from io import BytesIO
import pytest
from PIL import Image
from app.db.models.users import Consent
from tests.test_reporting import payload
@pytest.mark.skipif(os.environ.get("RUN_STORAGE_TESTS")!="1",reason="Requires a local MinIO instance")
def test_real_private_storage_upload_retry_and_read(client,account,db,monkeypatch):
    monkeypatch.setattr("app.routers.citizen.reverse",lambda *a:{"source":"user_provided","address":None})
    user,h=account();_,other=account()
    db.add(Consent(user_id=user.id,purpose="account_and_reporting"));db.commit()
    n=client.post("/api/v1/citizen/needs",headers=h,json=payload()).json()
    raw=BytesIO();Image.new("RGB",(12,12),"green").save(raw,format="PNG")
    args={"headers":h,"files":{"file":("test.png",raw.getvalue(),"image/png")}}
    first=client.post("/api/v1/citizen/needs/"+n["id"]+"/media",**args)
    assert first.status_code==200,first.text
    second=client.post("/api/v1/citizen/needs/"+n["id"]+"/media",**args)
    assert second.json()["id"]==first.json()["id"]
    id=first.json()["id"];response=client.get("/api/v1/citizen/media/"+id,headers=h)
    assert response.status_code==200 and response.headers["content-type"]=="image/jpeg"
    assert Image.open(BytesIO(response.content)).size==(12,12)
    assert client.get("/api/v1/citizen/media/"+id,headers=other).status_code==404
    assert client.get("/api/v1/projects/evidence/"+id+"/media").status_code==404
