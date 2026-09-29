import pytest
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.modules.users.schemas import UserCreate


@pytest.mark.asyncio
async def test_create_user_happy_path(db_session):
    repository = UserRepository(db_session)
    service = UserService(repository)

    data = UserCreate(
        username="testuser",
        password="password123",
    )

    result = await service.create_user(data)

    assert result.username == "testuser"
    assert result.password_hash != "password123"
    assert result.id is not None
    assert result.username is not None
    assert result.password_hash is not None