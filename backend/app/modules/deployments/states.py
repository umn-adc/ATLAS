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
    {
        DeploymentStatus.STOPPED,
        DeploymentStatus.FAILED,
        DeploymentStatus.CRASHED,
    }
)


# Define all permitted deployment state transitions.
ALLOWED_TRANSITIONS = {
    DeploymentStatus.PENDING: {
        DeploymentStatus.STARTING,
        DeploymentStatus.FAILED,
    },
    DeploymentStatus.STARTING: {
        DeploymentStatus.RUNNING,
        DeploymentStatus.FAILED,
    },
    DeploymentStatus.RUNNING: {
        DeploymentStatus.STOPPING,
        DeploymentStatus.CRASHED,
    },
    DeploymentStatus.STOPPING: {
        DeploymentStatus.STOPPED,
        DeploymentStatus.CRASHED,
    },
}


def can_transition(
    current: DeploymentStatus,
    target: DeploymentStatus,
) -> bool:
    """Check whether a deployment status transition is allowed."""

    if current in TERMINAL_STATUSES:
        return False

    return target in ALLOWED_TRANSITIONS.get(current, set())
