"""Tests for the views router."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# === Create ===


# TODO: may be blocked by another issue??? cannot get a request through...
def test_create_user():
    response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == "testuser"
    assert "password" not in body
    assert "password_hash" not in body
