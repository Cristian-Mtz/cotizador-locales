from __future__ import annotations
from tests.factories import locale_doc

def test_locales_pagination_and_total_pages(client, mongo_sync):
    col = mongo_sync["locales"]
    col.delete_many({})
    col.insert_many([locale_doc(codigo=f"L-A-{i:03d}") for i in range(1, 13)])

    r = client.get("/api/locales?page=1&page_size=10")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 12
    assert data["total_pages"] == 2
    assert len(data["items"]) == 10

def test_locales_filters(client, mongo_sync):
    col = mongo_sync["locales"]
    col.delete_many({})
    col.insert_many([
        locale_doc(codigo="L-A-001", pabellon="A", precio_mensual=15000, area_m2=40),
        locale_doc(codigo="L-B-001", pabellon="B", precio_mensual=25000, area_m2=60),
    ])

    r = client.get("/api/locales?pabellon=B")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["codigo"] == "L-B-001"

def test_local_detail_404(client, mongo_sync):
    mongo_sync["locales"].delete_many({})
    r = client.get("/api/locales/NO-EXISTE")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "LOCAL_NOT_FOUND"
