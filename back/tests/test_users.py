from fastapi.testclient import TestClient

from app.main import app


def test_users_endpoint():
    with TestClient(app) as client:
        r = client.get("/api/users")
        assert r.status_code in (200, 503)
