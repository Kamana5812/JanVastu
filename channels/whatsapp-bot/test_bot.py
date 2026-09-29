"""Contract check for the local adapter. Provider delivery is out of scope."""
from fastapi.testclient import TestClient
from main import app
def test_missing_authorization_and_consent_rejected():
    client=TestClient(app)
    assert client.post("/webhook",json={"description":"A synthetic water report."}).status_code==422
    assert client.get("/health").json()["provider_connected"] is False
