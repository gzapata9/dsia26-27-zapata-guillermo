import os

from api_robusta import app


def test_analyze_ok(monkeypatch):
    monkeypatch.delenv("FORCE_AI_FAIL", raising=False)
    res = app.test_client().post("/analyze", json={"text": "hola mundo de prueba robusta"})
    assert res.status_code == 200
    assert "request_id" in res.get_json()


def test_analyze_provider_fail(monkeypatch):
    monkeypatch.setenv("FORCE_AI_FAIL", "1")
    res = app.test_client().post("/analyze", json={"text": "hola"})
    assert res.status_code == 503
    assert "request_id" in res.get_json()
