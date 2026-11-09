"""Build the command the daemon runs to launch a strategy version."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LaunchSpec:
    """Everything the daemon needs to start a strategy process."""

    argv: list[str]
    cwd: Path
    env: dict[str, str] = field(default_factory=dict)


def build_launch_spec(
    artifact_path: Path,
    entrypoint: str,
    parameters: dict[str, Any],
) -> LaunchSpec:
    """
    Build the launch command for a strategy version.

    Args:
        artifact_path: Directory holding the version's stored code
        entrypoint: Entrypoint file, relative to artifact_path
        parameters: The version's strategy parameters

    Returns:
        LaunchSpec: Command, working directory and environment for the process

    Raises:
        ValueError: If the entrypoint resolves outside artifact_path

    Implementation:
        Resolve the entrypoint inside artifact_path and reject paths that escape it.
        Run it with the Python interpreter, with artifact_path as the working directory.
        Pass parameters to the process (e.g. as a JSON env var).
    """
    raise NotImplementedError
