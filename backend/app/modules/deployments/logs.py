"""Log file locations for running strategy processes."""

from pathlib import Path
from uuid import UUID

LOGS_PATH = Path("data/deployments")


def get_log_path(deployment_id: UUID) -> Path:
    """
    Return the log file path for a deployment.

    Args:
        deployment_id: Deployment identifier

    Returns:
        Path to the deployment's log file
    """
    raise NotImplementedError


def tail_lines(path: Path, n: int = 100) -> list[str]:
    """
    Return the last n lines of a log file.

    Args:
        path: Log file to read
        n: Number of lines to return

    Returns:
        list[str]: Up to n lines, oldest first. Empty if the file doesn't exist.

    Raises:
        ValueError: If n < 1
    """
    raise NotImplementedError
