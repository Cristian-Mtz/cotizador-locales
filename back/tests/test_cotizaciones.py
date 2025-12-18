from __future__ import annotations
from tests.factories import locale_doc

def test_post_cotizacion_happy_path(client, mongo_sync):
    mongo_sync["locales"].delete_many({})
    mongo_sync["cotizaciones"].delete_many({})
    mongo_sync["locales"].insert_one(locale_doc(codigo="L-A-001", precio_mensual=15000, status="disponible"))

    r = client.post("/api/cotizaciones", json={
        "prospecto_email": "Demo@Mail.com",
        "local_codigo": "l-a-001",
        "duracion_meses": 6,
        "notas": "Prueba",
    })
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"]
    assert data["prospecto_email"] == "demo@mail.com"
    assert data["local_codigo"] == "L-A-001"
    assert data["subtotal"] == 90000
    assert data["iva"] == 14400
    assert data["total"] == 104400

def test_post_cotizacion_local_not_found(client, mongo_sync):
    mongo_sync["locales"].delete_many({})
    r = client.post("/api/cotizaciones", json={"prospecto_email":"a@a.com","local_codigo":"L-X-999","duracion_meses":1,"notas":""})
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "LOCAL_NOT_FOUND"

def test_post_cotizacion_local_not_available(client, mongo_sync):
    mongo_sync["locales"].delete_many({})
    mongo_sync["locales"].insert_one(locale_doc(codigo="L-A-001", status="ocupado"))
    r = client.post("/api/cotizaciones", json={"prospecto_email":"a@a.com","local_codigo":"L-A-001","duracion_meses":1,"notas":""})
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "LOCAL_NOT_AVAILABLE"

def test_list_cotizaciones_sorted_desc(client, mongo_sync):
    mongo_sync["locales"].delete_many({})
    mongo_sync["cotizaciones"].delete_many({})
    mongo_sync["locales"].insert_one(locale_doc(codigo="L-A-001", status="disponible"))

    client.post("/api/cotizaciones", json={"prospecto_email":"demo@mail.com","local_codigo":"L-A-001","duracion_meses":1,"notas":""})
    client.post("/api/cotizaciones", json={"prospecto_email":"demo@mail.com","local_codigo":"L-A-001","duracion_meses":2,"notas":""})

    r = client.get("/api/cotizaciones/prospecto/demo@mail.com")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert items[0]["duracion_meses"] == 2
