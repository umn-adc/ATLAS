"""
Artifact storage service for strategy code files.

Stores versioned copies of strategy code so backtesting and deployment
always use the exact code from that version.
"""

import shutil
from pathlib import Path
from uuid import UUID

from .errors import ArtifactExistsError, SourceNotFoundError


DATA_PATH = Path("data/strategies")


def get_path(strategy_id: UUID, version_id: UUID) -> Path:
    """
    Return Path to artifact directory for given strategy/version.

    Args:
        strategy_id: Strategy identifier
        version_id: Version identifier

    Returns:
        Path to artifact directory
    """
    return DATA_PATH / str(strategy_id) / str(version_id)


def exists(strategy_id: UUID, version_id: UUID) -> bool:
    """
    Check if artifact exists for given strategy/version.

    Args:
        strategy_id: Strategy identifier
        version_id: Version identifier

    Returns:
        True if artifact directory exists
    """
    return get_path(strategy_id, version_id).exists()


def save(strategy_id: UUID, version_id: UUID, source_path: str | Path) -> Path:
    """
    Copy strategy code files to managed artifact directory.

    Copies source file or directory to data/strategies/{strategy_id}/{version_id}/.
    Creates parent directories if needed.

    Args:
        strategy_id: Strategy identifier
        version_id: Version identifier
        source_path: Path to source file or directory to copy

    Returns:
        Path to artifact directory

    Raises:
        SourceNotFoundError: If source_path does not exist
        ArtifactExistsError: If artifact already exists for this version
    """
    source = Path(source_path)

    if not source.exists():
        raise SourceNotFoundError(str(source))

    if exists(strategy_id, version_id):
        raise ArtifactExistsError(strategy_id, version_id)

    artifact_dir = get_path(strategy_id, version_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    if source.is_dir():
        # Copy directory contents into artifact directory
        shutil.copytree(source, artifact_dir, dirs_exist_ok=True)
    else:
        # Copy single file into artifact directory
        shutil.copy2(source, artifact_dir / source.name)

    return artifact_dir
