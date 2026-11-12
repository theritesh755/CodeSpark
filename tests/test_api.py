from fastapi.testclient import TestClient
from main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_security_capabilities():
    with TestClient(app) as client:
        response = client.get("/api/v1/security/capabilities")
        assert response.status_code == 200
        assert "hash-chained-audit-log" in response.json()["controls"]
