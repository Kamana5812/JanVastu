import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import engine, SessionLocal
from app.db.models.users import User, UserRole, UserStatus, uid
from app.core.security import get_password_hash, create_token

if not engine.url.database or not engine.url.database.endswith(("_test","_verification")):
    raise RuntimeError("Tests require a database ending in _test or _verification.")

@pytest.fixture
def client():
    with TestClient(app, client=(uid(),50000)) as client:
        yield client

@pytest.fixture
def db():
    with SessionLocal() as session:
        yield session

@pytest.fixture
def account(db):
    def make(role="citizen", state="Odisha", district="Puri", status="active"):
        user = User(name="Synthetic Test User", email=uid()+"@example.org", mobile=None,
            password_hash=get_password_hash("Test-password-27"), role=UserRole(role), status=UserStatus(status),
            state=state, district=district, preferred_language="en")
        db.add(user); db.commit()
        return user, {"Authorization":"Bearer "+create_token(user)}
    return make
