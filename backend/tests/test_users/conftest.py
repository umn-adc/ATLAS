"""Fixtures for User tests."""

from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models_base import Base

from app.modules.users.service import UserService
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate

# === Database Fixtures (for repository tests) ===


@pytest_asyncio.fixture
async def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# === Service Fixtures (for service tests) ===
# TODO: Replace with real service once repository is implemented

@pytest.fixture
def service():
    """Return a UserService instance."""
    return UserService()

@pytest.fixture
def service_with_data(service):

    user = UserCreate(
        username="testuser",
        password="password123",
    )

    return service, user