from datetime import datetime
from uuid import UUID

from app.modules.audit_logs.schemas import (
    AuditEventCreate,
    AuditEvent,
    Actor
)

from app.modules.audit_logs.repository import AuditRepository


class AuditService:


    def __init__(self, repository: AuditRepository):
            self.repository = repository


    def log_action(self, user_id: UUID, action: str, actor: Actor, created_at: datetime, details: dict) -> AuditEvent:
        """Records a new audit event"""

        #returns created logs from repository...
        raise NotImplementedError

    def get_logs(self, user_id: UUID, before_datetime: datetime) -> list[AuditEvent]:
        """Get user logs"""

        #returns logs from repository...
        raise NotImplementedError

    def get_resource_logs(self, resource_type: str, resource_id: str, user_id: UUID, before_datetime: datetime ) -> list[AuditEvent]:
        """Gets logs from a specific resource type"""

        #returns specific type of logs from repository...
        raise NotImplementedError

