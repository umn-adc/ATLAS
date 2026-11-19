import pytest

from fastapi.testclient import TestClient

from app.main import create_app
from app.database.base import get_db

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_health_database_ok(app, client):
    class FakeDB: 
        async def execute(self, statement):
            assert str(statement) == "SELECT 1"

    app.dependency_overrides[get_db] = lambda: FakeDB()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "version": app.version,
        "database_status": "ok",
    }

def test_health_database_unreachable(app, client):
    class FakeDB:
        async def execute(self):
            raise RuntimeError("Database unavailable")

    app.dependency_overrides[get_db] = lambda: FakeDB()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "version": app.version,
        "database_status": "unreachable",
    }