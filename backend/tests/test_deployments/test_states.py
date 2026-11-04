"""Tests for deployment lifecycle status transitions."""

import pytest

from app.modules.deployments.states import (
    TERMINAL_STATUSES,
    DeploymentStatus,
    can_transition,
)

# Expected lifecycle rules from issue #134.
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
    DeploymentStatus.STOPPED: set(),
    DeploymentStatus.FAILED: set(),
    DeploymentStatus.CRASHED: set(),
}


@pytest.mark.parametrize(
    ("current", "target", "expected"),
    [
        (current, target, target in allowed_targets)
        for current, allowed_targets in ALLOWED_TRANSITIONS.items()
        for target in DeploymentStatus
    ],
)
def test_can_transition(current, target, expected):
    """Every status transition must follow the defined lifecycle rules."""
    assert can_transition(current, target) is expected


def test_terminal_statuses():
    """Only stopped, failed and crashed are terminal states."""
    assert TERMINAL_STATUSES == {
        DeploymentStatus.STOPPED,
        DeploymentStatus.FAILED,
        DeploymentStatus.CRASHED,
    }
