"""Pre-deploy checks for stored strategy artifacts."""

from pathlib import Path


def verify_entrypoint(artifact_path: Path, entrypoint: str) -> Path:
    """
    Confirm the entrypoint file exists inside the artifact directory.

    Args:
        artifact_path: Directory holding the version's stored code
        entrypoint: Entrypoint file, relative to artifact_path

    Returns:
        Path: Resolved path to the entrypoint

    Raises:
        FileNotFoundError: If the entrypoint file doesn't exist
        ValueError: If the entrypoint resolves outside artifact_path
    """
    raise NotImplementedError


def compute_checksum(artifact_path: Path) -> str:
    """
    Return a SHA-256 checksum covering every file in the artifact directory.

    Args:
        artifact_path: Directory holding the version's stored code

    Returns:
        str: Hex digest. Same files and contents always give the same digest,
            regardless of filesystem ordering.
    """
    raise NotImplementedError
