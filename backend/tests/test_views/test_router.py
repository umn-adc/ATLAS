"""Tests for the views router."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# === Create ===


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


# === Get Single ===


def test_get_view():
    create_resp = client.post("/api/views/", json={"name": "Test View"})
    view_id = create_resp.json()["id"]

    response = client.get(f"/api/views/{view_id}")

    assert response.status_code == 200
    assert response.json()["id"] == view_id
    assert response.json()["name"] == "Test View"


def test_get_view_not_found():
    response = client.get("/api/views/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


# === Update ===


def test_update_view_name():
    create_resp = client.post("/api/views/", json={"name": "Original"})
    view_id = create_resp.json()["id"]

    response = client.patch(f"/api/views/{view_id}", json={"name": "Updated"})

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_update_view_layout():
    create_resp = client.post("/api/views/", json={"name": "Test"})
    view_id = create_resp.json()["id"]

    new_layout = {"cards": []}
    response = client.patch(f"/api/views/{view_id}", json={"layout": new_layout})

    assert response.status_code == 200
    assert response.json()["layout"] == new_layout


def test_update_view_not_found():
    response = client.patch(
        "/api/views/00000000-0000-0000-0000-000000000000",
        json={"name": "Ghost"},
    )

    assert response.status_code == 404


# === Delete ===


def test_delete_view():
    create_resp = client.post("/api/views/", json={"name": "To Delete"})
    view_id = create_resp.json()["id"]

    response = client.delete(f"/api/views/{view_id}")

    assert response.status_code == 204

    # Verify it's gone
    get_resp = client.get(f"/api/views/{view_id}")
    assert get_resp.status_code == 404


def test_delete_view_not_found():
    response = client.delete("/api/views/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
