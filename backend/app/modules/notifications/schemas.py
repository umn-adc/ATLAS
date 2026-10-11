from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime
from app.modules.notifications.models import NotificationType

from uuid import UUID

class NotificationCreate(BaseModel):
    owner_id: UUID     
    type: NotificationType     
    title: str = Field(max_length=50)     
    message: str | None = Field(default=None, max_length=500)     
    data: dict[str, Any] = Field(default_factory=dict)


class NotificationUpdate(BaseModel):
    id: UUID
    user_id: UUID
    read_at: datetime


class Notification(BaseModel):
    id: UUID
    user_id: UUID
    type: NotificationType     # deployment_complete, strategy_shared, etc.
    title: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=500)
    data: Dict | None = None    # related IDs, links
    read_at: datetime | None = None # null = unread
    created_at: datetime
    