import pytest
from fastapi.testclient import TestClient

from Workshop import router


@pytest.fixture
def client() -> TestClient:
    from Workshop.main import app

    router.reset()
    return TestClient(app)


# BEGINNER
def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_create_pet(client: TestClient) -> None:
    r = client.post("/pets", json={"name": "Buddy", "animal": "dog", "age": 3})
    assert r.json()["id"] == 1


def test_list_pets(client: TestClient) -> None:
    client.post("/pets", json={"name": "Buddy", "animal": "dog", "age": 3})
    assert len(client.get("/pets").json()) == 1


# MEDIUM
def test_get_pet_by_id(client: TestClient) -> None:
    client.post("/pets", json={"name": "Buddy", "animal": "dog", "age": 3})
    assert client.get("/pets/1").json()["name"] == "Buddy"


def test_get_pet_404(client: TestClient) -> None:
    assert client.get("/pets/999").status_code == 404


def test_delete_pet(client: TestClient) -> None:
    client.post("/pets", json={"name": "Buddy", "animal": "dog", "age": 3})
    assert client.delete("/pets/1").json() == {"deleted": 1}
    assert client.get("/pets").json() == []


# HARD
def test_search_by_animal(client: TestClient) -> None:
    client.post("/pets", json={"name": "Buddy", "animal": "dog", "age": 3})
    client.post("/pets", json={"name": "Whiskers", "animal": "cat", "age": 2})
    dogs = client.get("/pets/search/?animal=dog").json()
    assert len(dogs) == 1
    assert dogs[0]["name"] == "Buddy"


def test_search_by_age_range(client: TestClient) -> None:
    client.post("/pets", json={"name": "Puppy", "animal": "dog", "age": 1})
    client.post("/pets", json={"name": "Adult", "animal": "dog", "age": 5})
    client.post("/pets", json={"name": "Senior", "animal": "dog", "age": 12})
    result = client.get("/pets/search/?min_age=2&max_age=10").json()
    assert len(result) == 1
    assert result[0]["name"] == "Adult"


def test_negative_age_rejected(client: TestClient) -> None:
    r = client.post("/pets", json={"name": "Bad", "animal": "dog", "age": -5})
    assert r.status_code == 422
