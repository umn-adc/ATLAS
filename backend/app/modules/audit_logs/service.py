from datetime import datetime, timezone
from uuid import UUID

from app.modules.audit_logs.schemas import (
    AuditEventCreate,
    WarningLevel
)
from app.modules.audit_logs.models import AuditEvent as AuditEventModel

from app.modules.audit_logs.repository import AuditRepository
from backend.app.modules.audit_logs.errors import LogsNotFoundError


class AuditService:


    def __init__(self, repository: AuditRepository):
            self.repository = repository

    async def log_action(self, user_id, data: AuditEventCreate, details: dict | None = None, warning_level: int | WarningLevel = 0,) -> AuditEventModel:
        """Records a new audit event and commits the transaction."""
        #No use for user_id or timestamp?

        target_id = data.target.id if data.target else None
        target_type = data.target.type if data.target else None

        timestamp = datetime.now(timezone.utc)

        event = await self.repository.create(
            action=data.action,
            actor_id=data.actor.id,
            actor_type=data.actor.type,
            outcome=data.outcome,
            target_id=target_id,
            target_type=target_type,
            details=details,
            warning_level=int(warning_level),
        )

        await self.repository.session.commit()

        return event

    async def get_log_by_id(self, log_id: UUID) -> AuditEventModel:
        """Fetch a single audit log by ID"""
        event = await self.repository.get_by_id(log_id)
        if not event:
            raise LogsNotFoundError(log_id=log_id)
        return event

    async def get_logs_by_action(self, action: str) -> list[AuditEventModel]:
        """Fetch all audit logs for a given action"""
        return await self.repository.list_by_action(action)

    async def get_logs_by_actor(self, actor_id: UUID) -> list[AuditEventModel]:
        """Fetch all audit logs associated with a specific actor"""
        return await self.repository.list_by_actor(actor_id)

    async def get_logs_by_target(self, target_id: UUID) -> list[AuditEventModel]:
        """Fetch all audit logs performed against a specific target resource."""
        event = await self.repository.list_by_target(target_id)
        if not event:
            raise LogsNotFoundError(log_id=target_id)
        return event

    async def get_logs_by_warning(self, warning_level: int) -> list[AuditEventModel]:
        """Fetch all audit logs matching or exceeding a warning level."""
        return await self.repository.list_by_warning(warning_level)

