"""Fixtures for strategy tests."""

from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models_base import Base
from app.modules.strategies.service import StrategyService

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
    """Return a StrategyService instance."""
    return StrategyService()


@pytest.fixture
def service_with_data(service):
    """Return service with one strategy created.

    Returns: (service, owner_id, strategy_id)

    TODO: Wire up real repository when implemented.
    """
    # This fixture will work once create_strategy is implemented
    # For now, tests will fail with NotImplementedError - that's expected
    owner_id = uuid4()
    from app.modules.strategies.schemas import StrategyCreate

    strategy = service.create_strategy(owner_id, StrategyCreate(name="Test Strategy"))
    return service, owner_id, strategy.id


@pytest.fixture
def service_with_archived(service):
    """Return service with one active and one archived strategy.

    Returns: (service, owner_id)

    TODO: Wire up real repository when implemented.
    """
    owner_id = uuid4()
    from app.modules.strategies.schemas import StrategyCreate

    service.create_strategy(owner_id, StrategyCreate(name="Active"))
    strategy = service.create_strategy(owner_id, StrategyCreate(name="To Archive"))
    service.archive_strategy(strategy.id, owner_id)
    return service, owner_id


@pytest.fixture
def service_with_version(service_with_data):
    """Return service with a strategy that has one version.

    Returns: (service, owner_id, strategy_id)
    """
    service, owner_id, strategy_id = service_with_data
    from app.modules.strategies.schemas import StrategyVersionCreate

    service.create_version(
        strategy_id,
        owner_id,
        StrategyVersionCreate(
            commit_hash="abc123",
            entrypoint="main.py",
            artifact_path="/data/artifacts/test",
            parameters={},
        ),
    )
    return service, owner_id, strategy_id
