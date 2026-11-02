from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint_is_live():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_dashboard_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Compare with your baseline" in response.text


def test_prediction_endpoint_returns_research_notice():
    response = client.post(
        "/api/v1/predict",
        json={"steps_deviation_7d_pct": 0, "sleep_deviation_7d_pct": 0},
    )
    assert response.status_code == 200
    assert "not a diagnosis" in response.json()["notice"]


def test_prediction_rejects_out_of_range_input():
    response = client.post(
        "/api/v1/predict",
        json={"steps_deviation_7d_pct": -101, "sleep_deviation_7d_pct": 0},
    )
    assert response.status_code == 422


def test_prediction_rejects_nan():
    response = client.post(
        "/api/v1/predict",
        content='{"steps_deviation_7d_pct": NaN, "sleep_deviation_7d_pct": 0}',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_security_headers_are_present():
    response = client.get("/api/v1/health")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]


def test_evidence_endpoint_returns_sources():
    response = client.post(
        "/api/v1/ask", json={"question": "How much activity do adults need?"}
    )
    assert response.status_code == 200
    assert response.json()["sources"]
    assert "cdc.gov" in response.json()["sources"][0]["url"]


def test_evidence_endpoint_rejects_blank_question():
    response = client.post("/api/v1/ask", json={"question": "   "})
    assert response.status_code == 422


def test_insight_workflow_requires_at_least_two_observation_windows():
    response = client.post("/api/v1/insights/analyze", json={"observations": []})
    assert response.status_code == 422


def test_readiness_returns_service_unavailable_when_database_is_down(monkeypatch):
    from backend.routes import health

    def unavailable():
        raise OSError("database unavailable")

    monkeypatch.setattr(health.engine, "connect", unavailable)
    monkeypatch.setattr(health, "model_is_available", lambda: True)
    response = client.get("/api/v1/ready")
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
