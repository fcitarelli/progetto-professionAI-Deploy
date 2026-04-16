from fastapi.testclient import TestClient
from API.modelPrediction import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_sentiment():
    with TestClient(app) as client:
        response = client.post("/predict", json={"review": "This product is amazing!"})

    assert response.status_code == 200
    body = response.json()
    assert "sentiment" in body
    assert "confidence" in body
    assert isinstance(body["sentiment"], str)
    assert isinstance(body["confidence"], float)
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_empty_review():
    with TestClient(app) as client:
        response = client.post("/predict", json={"review": ""})

    assert response.status_code == 400


def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "api_requests_total" in response.text
