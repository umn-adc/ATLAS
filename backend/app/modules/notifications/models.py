from app.database.base import Base

from sqlalchemy.orm import Mapped

from datetime import datetime

from uuid import UUID


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID]
    user_id: Mapped[UUID]
    type: Mapped[str]              # deployment_complete, strategy_shared, etc.
    title: Mapped[str]
    message: Mapped[str]
    data: Mapped[dict | None]      # related IDs, links
    read_at: Mapped[datetime | None]  # null = unread
    created_at: Mapped[datetime]