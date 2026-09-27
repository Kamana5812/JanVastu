from app.core.security import create_token
from app.db.models.users import UserStatus, AccessRequest
from sqlalchemy import text
import pytest

def test_token_type_status_and_role(client, account, db):
    user, headers = account()
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 200
    assert client.get("/api/v1/admin/users", headers=headers).status_code == 403
    assert client.get("/api/v1/auth/me", headers={"Authorization":"Bearer "+create_token(user, "refresh")}).status_code == 401
    user.status = UserStatus.suspended; db.commit()
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 401

def test_approval_and_mfa(client, account, db):
    admin, headers = account("admin")
    volunteer, vheaders = account("volunteer", status="pending_approval")
    application = AccessRequest(user_id=volunteer.id, role_requested="volunteer", status="pending")
    db.add(application); db.commit()
    assert client.get("/api/v1/auth/me", headers=vheaders).status_code == 401
    assert client.patch(f"/api/v1/admin/users/{volunteer.id}/status", headers=headers, json={"status":"active"}).status_code == 200
    db.refresh(application); assert application.status == "approved"
    response = client.post("/api/v1/admin/login", json={"identifier":admin.email, "password":"Test-password-27"})
    assert response.status_code == 200
    challenge = response.json()["challenge_id"]
    assert client.post("/api/v1/auth/otp/verify", json={"challenge_id":challenge, "code":"000000"}).status_code == 400
    verified = client.post("/api/v1/auth/otp/verify", json={"challenge_id":challenge, "code":"123456"})
    assert verified.status_code == 200 and "access_token" in verified.json()
    assert client.post("/api/v1/auth/otp/verify", json={"challenge_id":challenge, "code":"123456"}).status_code == 400

def test_refresh_rotation(client, account):
    user, _ = account()
    response = client.post("/api/v1/auth/login", json={"identifier":user.email, "password":"Test-password-27"})
    refresh = response.json()["refresh_token"]
    assert client.post("/api/v1/auth/refresh", json={"refresh_token":refresh}).status_code == 200
    assert client.post("/api/v1/auth/refresh", json={"refresh_token":refresh}).status_code == 401

def test_public_admin_request_rejected(client):
    response = client.post("/api/v1/auth/access-request", json={
        "name":"Synthetic Applicant", "email":"invalid-role@example.org", "password":"Test-password-27",
        "state":"Odisha","district":"Puri","consent":True,"role_requested":"admin",
        "organization":"Demo office","designation":"Demo","reason":"Synthetic test application",
        "verification_info":"Demo reference"})
    assert response.status_code == 422

def test_audit_immutable(client, account, db):
    user, _ = account()
    client.post("/api/v1/auth/login", json={"identifier":user.email,"password":"Test-password-27"})
    with pytest.raises(Exception, match="append-only"):
        db.execute(text("UPDATE audit_logs SET result='changed'"))
        db.commit()
    db.rollback()
