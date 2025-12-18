def test_validation_envelope(client):
    r = client.post("/api/cotizaciones", json={"prospecto_email":"a@a.com","local_codigo":"L-A-001","duracion_meses":0,"notas":""})
    assert r.status_code == 422
    payload = r.json()
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in payload["error"]
