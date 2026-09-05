from app import app


def test_health():
    assert app.test_client().get("/health").status_code == 200


def test_analyze_ok():
    res = app.test_client().post(
        "/analyze",
        json={"text": "uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece"},
    )
    assert res.status_code == 200
    body = res.get_json()
    assert "summary" in body
    assert body["provider"] == "mock"


def test_analyze_empty():
    res = app.test_client().post("/analyze", json={"text": "  "})
    assert res.status_code == 400
