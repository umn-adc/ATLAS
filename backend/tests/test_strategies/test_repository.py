"""Tests for strategy repository - shows what's implemented vs NotImplementedError."""

from uuid import uuid4

import pytest

from app.modules.strategies.repository import StrategyRepository, StrategyVersionRepository


# === StrategyRepository Tests ===


@pytest.mark.asyncio
async def test_create_strategy(db_session):
    repo = StrategyRepository(db_session)
    owner_id = uuid4()

    strategy = await repo.create(owner_id, "My Strategy", "A test strategy")

    assert strategy.name == "My Strategy"
    assert strategy.description == "A test strategy"
    assert strategy.owner_id == owner_id
    assert strategy.id is not None
    assert strategy.archived_at is None


@pytest.mark.asyncio
async def test_get_by_id_found(db_session):
    repo = StrategyRepository(db_session)
    created = await repo.create(uuid4(), "Test", None)

    found = await repo.get_by_id(created.id)

    assert found is not None
    assert found.id == created.id


@pytest.mark.asyncio
async def test_get_by_id_not_found(db_session):
    repo = StrategyRepository(db_session)

    found = await repo.get_by_id(uuid4())

    assert found is None


@pytest.mark.asyncio
async def test_list_by_owner(db_session):
    repo = StrategyRepository(db_session)
    owner_id = uuid4()
    other_owner = uuid4()
    await repo.create(owner_id, "Mine 1", None)
    await repo.create(owner_id, "Mine 2", None)
    await repo.create(other_owner, "Not Mine", None)

    strategies = await repo.list_by_owner(owner_id)

    assert len(strategies) == 2
    assert all(s.owner_id == owner_id for s in strategies)


@pytest.mark.asyncio
async def test_list_by_owner_excludes_archived(db_session):
    repo = StrategyRepository(db_session)
    owner_id = uuid4()
    active = await repo.create(owner_id, "Active", None)
    archived = await repo.create(owner_id, "Archived", None)
    # Manually archive one
    from datetime import datetime, timezone

    archived.archived_at = datetime.now(timezone.utc)
    await repo.update(archived)

    strategies = await repo.list_by_owner(owner_id, include_archived=False)

    assert len(strategies) == 1
    assert strategies[0].id == active.id


@pytest.mark.asyncio
async def test_update_strategy(db_session):
    repo = StrategyRepository(db_session)
    strategy = await repo.create(uuid4(), "Original", None)
    strategy.name = "Updated"

    updated = await repo.update(strategy)

    assert updated.name == "Updated"


# === StrategyVersionRepository Tests ===


@pytest.mark.asyncio
async def test_create_version(db_session):
    strategy_repo = StrategyRepository(db_session)
    version_repo = StrategyVersionRepository(db_session)
    strategy = await strategy_repo.create(uuid4(), "Test", None)

    version = await version_repo.create(
        strategy_id=strategy.id,
        commit_hash="abc123",
        entrypoint="main.py",
        artifact_path="/data/artifacts/test",
        parameters={"param1": "value1"},
    )

    assert version.strategy_id == strategy.id
    assert version.commit_hash == "abc123"
    assert version.entrypoint == "main.py"
    assert version.artifact_path == "/data/artifacts/test"
    assert version.parameters == {"param1": "value1"}


@pytest.mark.asyncio
async def test_list_by_strategy(db_session):
    strategy_repo = StrategyRepository(db_session)
    version_repo = StrategyVersionRepository(db_session)
    strategy = await strategy_repo.create(uuid4(), "Test", None)
    await version_repo.create(strategy.id, "hash1", "main.py", "/path1", {})
    await version_repo.create(strategy.id, "hash2", "main.py", "/path2", {})

    versions = await version_repo.list_by_strategy(strategy.id)

    assert len(versions) == 2
