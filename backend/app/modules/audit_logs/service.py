from datetime import datetime
from uuid import UUID

from app.modules.audit_logs.schemas import (
    AuditEventCreate,
    AuditEvent,
    WarningLevel
)

from app.modules.audit_logs.repository import AuditRepository


class AuditService:


    def __init__(self, repository: AuditRepository):
            self.repository = repository


    def log_action(self, user_id: UUID, warning_level: Warning, data: AuditEventCreate) -> AuditEvent:
        """Records a new audit event"""
        action = data.action
        actor = data.actor
        target = data.target
        outcome = data.outcome
        timestamp = datetime.now() #Needs timezone info

        # id: UUID # unique id
        #     details: dict # JSON - old/new values
        #     warning_level: WarningLevel # degree of severity/attention needed
        #     schema_version: int = 1 # records iterations of schema


        return self.repository.create()
        #raise NotImplementedError

    def get_logs(self, user_id: UUID, before_datetime: datetime) -> list[AuditEvent]:
        """Get user logs"""

        #returns logs from repository...
        raise NotImplementedError

    def get_resource_logs(self, resource_type: str, resource_id: str, user_id: UUID, before_datetime: datetime ) -> list[AuditEvent]:
        """Gets logs from a specific resource type"""

        #returns specific type of logs from repository...
        raise NotImplementedError

