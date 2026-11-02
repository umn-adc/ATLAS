from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit_logs.models import AuditEvent
from app.modules.audit_logs.schemas import Outcome

class AuditRepository:
    """Database operations for audit logs."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        action: str,
        actor_id: UUID,
        actor_type: str,
        outcome: Outcome,
        target_id: UUID | None = None,
        target_type: str | None = None,
        details: dict | None = None,
        warning_level: int = 0
    ) -> AuditEvent:
        """Insert a new audit event and return it."""
        event = AuditEvent(
            action=action,
            actor_id=actor_id,
            actor_type=actor_type,
            target_id=target_id,
            target_type=target_type,
            outcome=outcome,
            details=details,
            warning_level=warning_level,
        )
        self.session.add(event)

        # save changes on current transaction
        # opted for flush() and refresh() instead of commit() #TODO: need to implement commit calls elsewhere
        # keeps changes within an open transaction, allowing for further calls and/or rollback if necessary
        await self.session.flush()
        await self.session.refresh(event)

        return event

    async def get_by_id(self, id: UUID) -> AuditEvent | None:
        """Return an audit event by ID, or None if not found."""
            
        return await self.session.get(AuditEvent, id)

    async def list_by_action(self, action: str) -> list[AuditEvent]:
        """Return all events for a specified action"""
        stmt = select(AuditEvent).where(AuditEvent.action == action)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_actor(self, actor_id: UUID) -> list[AuditEvent]:
        """Return all events with a specified actor"""
        stmt = select(AuditEvent).where(AuditEvent.actor_id == actor_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_target(self, target_id: UUID) -> list[AuditEvent]:
        """Return all events with a specified target"""
        stmt = select(AuditEvent).where(AuditEvent.target_id == target_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_warning(self, warning_level: int) -> list[AuditEvent]:
        """Return all events with a specified warning level"""
        stmt = select(AuditEvent).where(AuditEvent.warning_level == warning_level)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())