"""Tests for artifact storage."""

from uuid import uuid4

import pytest

from app.modules.strategies import artifact_storage
from app.modules.strategies.errors import ArtifactExistsError, SourceNotFoundError


@pytest.fixture
def mock_data_path(tmp_path, monkeypatch):
    """Override DATA_PATH to use temp directory."""
    monkeypatch.setattr(artifact_storage, "DATA_PATH", tmp_path)
    return tmp_path


@pytest.fixture
def source_file(tmp_path):
    """Create a source file to copy."""
    src = tmp_path / "source" / "strategy.py"
    src.parent.mkdir(parents=True)
    src.write_text("def run(): pass")
    return src


@pytest.fixture
def source_dir(tmp_path):
    """Create a source directory to copy."""
    src = tmp_path / "source_dir"
    src.mkdir()
    (src / "main.py").write_text("def main(): pass")
    (src / "utils.py").write_text("def helper(): pass")
    return src


# === get_path ===


def test_get_path_returns_correct_structure(mock_data_path):
    strategy_id = uuid4()
    version_id = uuid4()

    result = artifact_storage.get_path(strategy_id, version_id)

    assert result == mock_data_path / str(strategy_id) / str(version_id)


# === exists ===


def test_exists_returns_false_when_missing(mock_data_path):
    assert artifact_storage.exists(uuid4(), uuid4()) is False


def test_exists_returns_true_when_present(mock_data_path):
    strategy_id = uuid4()
    version_id = uuid4()
    path = mock_data_path / str(strategy_id) / str(version_id)
    path.mkdir(parents=True)

    assert artifact_storage.exists(strategy_id, version_id) is True


# === save ===


def test_save_copies_single_file(mock_data_path, source_file):
    strategy_id = uuid4()
    version_id = uuid4()

    result = artifact_storage.save(strategy_id, version_id, source_file)

    assert result.exists()
    assert (result / source_file.name).read_text() == "def run(): pass"


def test_save_copies_directory(mock_data_path, source_dir):
    strategy_id = uuid4()
    version_id = uuid4()

    result = artifact_storage.save(strategy_id, version_id, source_dir)

    assert result.exists()
    assert (result / "main.py").read_text() == "def main(): pass"
    assert (result / "utils.py").read_text() == "def helper(): pass"


def test_save_creates_parent_directories(mock_data_path, source_file):
    strategy_id = uuid4()
    version_id = uuid4()

    result = artifact_storage.save(strategy_id, version_id, source_file)

    assert result.parent.exists()


def test_save_raises_on_missing_source(mock_data_path):
    with pytest.raises(SourceNotFoundError):
        artifact_storage.save(uuid4(), uuid4(), "/nonexistent/path")


def test_save_raises_on_existing_artifact(mock_data_path, source_file):
    strategy_id = uuid4()
    version_id = uuid4()

    artifact_storage.save(strategy_id, version_id, source_file)

    with pytest.raises(ArtifactExistsError):
        artifact_storage.save(strategy_id, version_id, source_file)
