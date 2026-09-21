"""Tests for the views router."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_view():
    response = client.post("/api/views/", json={"name": "My Dashboard"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "My Dashboard"
    assert body["layout"] == {"cards": []}
    assert "id" in body


def test_create_view_empty_name_rejected():
    response = client.post("/api/views/", json={"name": ""})

    assert response.status_code == 422
