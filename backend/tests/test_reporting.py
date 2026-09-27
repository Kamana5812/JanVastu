import uuid
from io import BytesIO
from PIL import Image
from app.db.models.users import Consent

def payload():
    return {"category":"water","description":"Water pipe is broken near the community well.",
        "latitude":19.81,"longitude":85.83,"state":"Odisha","district":"Puri",
        "client_id":str(uuid.uuid4()),"consent":True,"language":"en"}

def test_reporting_ownership_consent_and_retry(client,account,db,monkeypatch):
    monkeypatch.setattr("app.routers.citizen.reverse",lambda *args:{"source":"openstreetmap","address":"Test location"})
    user,headers=account();other,other_headers=account()
    data=payload()
    assert client.post("/api/v1/citizen/needs",headers=headers,json=data).status_code==403
    db.add(Consent(user_id=user.id,purpose="account_and_reporting"));db.commit()
    response=client.post("/api/v1/citizen/needs",headers=headers,json=data)
    assert response.status_code==200,response.text
    item=response.json()
    assert item["language"]=="en" and item["geocoding_source"]=="openstreetmap"
    assert client.post("/api/v1/citizen/needs",headers=headers,json=data).json()["id"]==item["id"]
    data["description"]="A different request with the same client identifier."
    assert client.post("/api/v1/citizen/needs",headers=headers,json=data).status_code==409
    assert client.get("/api/v1/citizen/needs/"+item["id"],headers=other_headers).status_code==404
    assert any(n["id"]==item["id"] for n in client.get("/api/v1/citizen/needs",headers=headers).json())
    assert not client.get("/api/v1/citizen/needs",headers=other_headers).json()
    assert client.get("/api/v1/citizen/needs/nearby?lat=19.81&lng=85.83",headers=headers).status_code==200
    assert client.post("/api/v1/citizen/needs/"+item["id"]+"/media",headers=headers,
        files={"file":("bad.jpg",b"not an image","image/jpeg")}).status_code==400
    raw=BytesIO();Image.new("RGB",(8,8),"red").save(raw,format="JPEG")
    uploads=[]
    monkeypatch.setattr("app.routers.citizen.put_media",lambda *args:uploads.append(args))
    uploaded=client.post("/api/v1/citizen/needs/"+item["id"]+"/media",headers=headers,
        files={"file":("evidence.jpg",raw.getvalue(),"image/jpeg")})
    assert uploaded.status_code==200 and len(uploads)==1

def test_input_bounds(client,account):
    _,headers=account();data=payload();data["latitude"]=100
    assert client.post("/api/v1/citizen/needs",headers=headers,json=data).status_code==422
    data=payload();data["consent"]=False
    assert client.post("/api/v1/citizen/needs",headers=headers,json=data).status_code==422

def test_multilingual_analysis_and_role_denial(client,account):
    _,headers=account()
    for text,category,language in [
        ("The water pipe is broken near the road.","water","en"),
        ("हमारे गांव में पानी नहीं आता है।","water","hi"),
        ("ଆମ ଗାଁରେ ପାଣି ଆସୁନାହିଁ।","water","or"),
        ("Hamare gaon ki sadak kharab hai","road","hi")]:
        r=client.post("/api/v1/citizen/analyze",headers=headers,json={"description":text})
        assert r.status_code==200 and r.json()["category"]==category and r.json()["language"]==language
    _,planner=account("district_official")
    assert client.post("/api/v1/citizen/analyze",headers=planner,json={"description":"The water pipe is broken."}).status_code==403
