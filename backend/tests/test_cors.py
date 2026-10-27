"""Tests for CORS middleware and the cors_origins setting."""

import pytest
from fastapi.testclient import TestClient

from app.database.base import Settings, settings
from app.main import app, create_app

client = TestClient(app)

ALLOWED = "http://localhost:5173"
DISALLOWED = "http://evil.example"


def preflight_headers(origin: str) -> dict[str, str]:
    return {
        "Origin": origin,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }


# === Simple Requests ===


def test_allowed_origin_gets_header():
    response = client.get("/api/health", headers={"Origin": ALLOWED})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED


def test_disallowed_origin_no_header():
    response = client.get("/api/health", headers={"Origin": DISALLOWED})

    assert "access-control-allow-origin" not in response.headers


# === Preflight ===


def test_preflight_allowed_origin():
    response = client.options("/api/views/", headers=preflight_headers(ALLOWED))

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED
    assert "POST" in response.headers["access-control-allow-methods"]


def test_preflight_disallowed_origin():
    response = client.options("/api/views/", headers=preflight_headers(DISALLOWED))

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


# === Settings ===


def test_default_origins(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("CORS_ORIGINS", raising=False)

    assert Settings(_env_file=None).cors_origins == [  # type: ignore[call-arg]
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@pytest.mark.parametrize(
    "env_value",
    ["http://a.com, http://b.com", '["http://a.com", "http://b.com"]'],
)
def test_env_var_parsing(monkeypatch: pytest.MonkeyPatch, env_value: str):
    monkeypatch.setenv("CORS_ORIGINS", env_value)

    assert Settings(_env_file=None).cors_origins == [  # type: ignore[call-arg]
        "http://a.com",
        "http://b.com",
    ]


def test_env_override_applies_to_app(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(settings, "cors_origins", ["https://atlas.example.com"])
    custom_client = TestClient(create_app())

    allowed = custom_client.get("/api/health", headers={"Origin": "https://atlas.example.com"})
    old_default = custom_client.get("/api/health", headers={"Origin": ALLOWED})

    assert allowed.headers["access-control-allow-origin"] == "https://atlas.example.com"
    assert "access-control-allow-origin" not in old_default.headers
