from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

class AuditLogCreate(BaseModel):
    id: Mapped[UUID]
    user_id: Mapped[UUID | None]       # null for system actions
    action: Mapped[str]                # create, update, delete, login
    resource_type: Mapped[str]         # strategy, user, deployment
    resource_id: Mapped[UUID | None]
    details: Mapped[dict]              # JSON - old/new values
    created_at: Mapped[datetime]
    warning_level: 