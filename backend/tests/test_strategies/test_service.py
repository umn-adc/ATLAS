"""Tests for strategy service - shows what's implemented vs NotImplementedError."""

from uuid import uuid4

import pytest

from app.modules.strategies.schemas import StrategyCreate, StrategyUpdate, StrategyVersionCreate

# === Beginner Tasks: get_strategy ===


def test_get_strategy_success(service_with_data):
    service, owner_id, strategy_id = service_with_data

    result = service.get_strategy(strategy_id, owner_id)

    assert result.id == strategy_id
    assert result.owner_id == owner_id


def test_get_strategy_not_found(service):
    with pytest.raises(ValueError, match="not found"):
        service.get_strategy(uuid4(), uuid4())


def test_get_strategy_wrong_owner(service_with_data):
    service, _, strategy_id = service_with_data
    other_user = uuid4()

    with pytest.raises(ValueError, match="doesn't own"):
        service.get_strategy(strategy_id, other_user)


# === Beginner Tasks: list_user_strategies ===


def test_list_user_strategies_returns_owned(service_with_data):
    service, owner_id, _ = service_with_data

    strategies = service.list_user_strategies(owner_id)

    assert len(strategies) >= 1
    assert all(s.owner_id == owner_id for s in strategies)


def test_list_user_strategies_excludes_archived(service_with_archived):
    service, owner_id = service_with_archived

    strategies = service.list_user_strategies(owner_id)

    assert all(s.archived_at is None for s in strategies)


def test_list_user_strategies_empty(service):
    strategies = service.list_user_strategies(uuid4())

    assert strategies == []


# === Beginner Tasks: update_strategy ===


def test_update_strategy_success(service_with_data):
    service, owner_id, strategy_id = service_with_data
    update = StrategyUpdate(name="New Name")

    result = service.update_strategy(strategy_id, owner_id, update)

    assert result.name == "New Name"


def test_update_strategy_wrong_owner(service_with_data):
    service, _, strategy_id = service_with_data
    other_user = uuid4()
    update = StrategyUpdate(name="Hacked")

    with pytest.raises(ValueError, match="doesn't own"):
        service.update_strategy(strategy_id, other_user, update)


def test_update_strategy_not_found(service):
    update = StrategyUpdate(name="Ghost")

    with pytest.raises(ValueError, match="not found"):
        service.update_strategy(uuid4(), uuid4(), update)


# === Beginner Tasks: archive_strategy ===


def test_archive_strategy_success(service_with_data):
    service, owner_id, strategy_id = service_with_data

    result = service.archive_strategy(strategy_id, owner_id)

    assert result.archived_at is not None


def test_archive_strategy_wrong_owner(service_with_data):
    service, _, strategy_id = service_with_data
    other_user = uuid4()

    with pytest.raises(ValueError, match="doesn't own"):
        service.archive_strategy(strategy_id, other_user)


def test_archive_strategy_not_found(service):
    with pytest.raises(ValueError, match="not found"):
        service.archive_strategy(uuid4(), uuid4())


# === Advanced Tasks: create_strategy ===


def test_create_strategy(service):
    owner_id = uuid4()
    data = StrategyCreate(name="New Strategy", description="Test")

    result = service.create_strategy(owner_id, data)

    assert result.name == "New Strategy"
    assert result.description == "Test"
    assert result.owner_id == owner_id


# === Advanced Tasks: create_version ===


def test_create_version_success(service_with_data):
    service, owner_id, strategy_id = service_with_data
    data = StrategyVersionCreate(
        commit_hash="abc123",
        entrypoint="main.py",
        artifact_path="/data/artifacts/test",
        parameters={"key": "value"},
    )

    result = service.create_version(strategy_id, owner_id, data)

    assert result.strategy_id == strategy_id
    assert result.commit_hash == "abc123"


def test_create_version_wrong_owner(service_with_data):
    service, _, strategy_id = service_with_data
    other_user = uuid4()
    data = StrategyVersionCreate(
        commit_hash="abc123",
        entrypoint="main.py",
        artifact_path="/path",
        parameters={},
    )

    with pytest.raises(ValueError, match="doesn't own"):
        service.create_version(strategy_id, other_user, data)


# === Advanced Tasks: list_versions ===


def test_list_versions_success(service_with_version):
    service, owner_id, strategy_id = service_with_version

    versions = service.list_versions(strategy_id, owner_id)

    assert len(versions) >= 1
    assert all(v.strategy_id == strategy_id for v in versions)


def test_list_versions_wrong_owner(service_with_data):
    service, _, strategy_id = service_with_data
    other_user = uuid4()

    with pytest.raises(ValueError, match="doesn't own"):
        service.list_versions(strategy_id, other_user)
