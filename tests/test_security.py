import pytest

from backend.security import allowed_origins


def test_local_cors_defaults(monkeypatch):
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    monkeypatch.setenv("APP_ENV", "development")
    assert allowed_origins() == ["http://localhost:5173", "http://localhost:3000"]


def test_wildcard_cors_is_rejected(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("CORS_ORIGINS", "*")
    with pytest.raises(RuntimeError, match="Wildcard"):
        allowed_origins()


def test_production_requires_https_allowlist(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:5173")
    with pytest.raises(RuntimeError, match="HTTPS"):
        allowed_origins()


def test_production_requires_configured_origin(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    with pytest.raises(RuntimeError, match="must be set"):
        allowed_origins()


def test_production_uses_platform_hostname(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    monkeypatch.setenv("RENDER_EXTERNAL_HOSTNAME", "health-ai-example.onrender.com")
    assert allowed_origins() == ["https://health-ai-example.onrender.com"]
