"""Interface the backend uses to talk to the atlasd daemon, plus an in-memory fake."""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.modules.deployments.launch_spec import LaunchSpec
from app.modules.deployments.states import DeploymentStatus


@dataclass(frozen=True)
class ProcessInfo:
    """What the daemon reports about one strategy process."""

    deployment_id: UUID
    status: DeploymentStatus
    pid: int | None
    returncode: int | None


class DaemonClient(Protocol):
    """Commands the backend can send to the daemon."""

    async def start(self, deployment_id: UUID, spec: LaunchSpec) -> ProcessInfo:
        """Start a strategy process for the deployment."""
        ...

    async def status(self, deployment_id: UUID) -> ProcessInfo:
        """Return the current state of a deployment's process."""
        ...

    async def list(self) -> list[ProcessInfo]:
        """Return every process the daemon is tracking."""
        ...

    async def stop(self, deployment_id: UUID) -> ProcessInfo:
        """Stop a deployment's process."""
        ...


class FakeDaemonClient:
    """
    In-memory DaemonClient for tests and local development.

    Tracks deployments in a dict instead of launching real processes.
    Unknown deployment IDs raise KeyError.
    """

    async def start(self, deployment_id: UUID, spec: LaunchSpec) -> ProcessInfo:
        raise NotImplementedError

    async def status(self, deployment_id: UUID) -> ProcessInfo:
        raise NotImplementedError

    async def list(self) -> list[ProcessInfo]:
        raise NotImplementedError

    async def stop(self, deployment_id: UUID) -> ProcessInfo:
        raise NotImplementedError
