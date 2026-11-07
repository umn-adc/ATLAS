"""Deployment lifecycle states and the transitions allowed between them."""

from enum import StrEnum


class DeploymentStatus(StrEnum):
    """Lifecycle state of a deployed strategy process."""

    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    CRASHED = "crashed"


TERMINAL_STATUSES = frozenset(
    {DeploymentStatus.STOPPED, DeploymentStatus.FAILED, DeploymentStatus.CRASHED}
)


def can_transition(current: DeploymentStatus, target: DeploymentStatus) -> bool:
    """
    Check whether a deployment may move from one status to another.

    Args:
        current: The deployment's current status
        target: The status it would move to

    Returns:
        bool: True if the transition is allowed

    Implementation:
        Define the allowed transitions (e.g. pending -> starting -> running -> stopping
        -> stopped, plus failure paths to failed / crashed).
        Terminal statuses cannot transition anywhere.
    """
    raise NotImplementedError
