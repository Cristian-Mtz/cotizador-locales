from fastapi.testclient import TestClient
from app.main import app

def test_get_local_detail():
    with TestClient(app) as client:
        r = client.get("/api/locales/L-A-001")
        assert r.status_code in (200, 503)  # 503 si mongo no está listo
