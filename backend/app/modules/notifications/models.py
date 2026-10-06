
from enum import StrEnum
from sqlalchemy import String, ForeignKey,DateTime,func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from uuid import UUID, uuid4

from app.database.base import Base

class NotifcationType(StrEnum):
    deployment_complete =  "deployment_complete"
    strategy_shared = "strategy_shared"
    #TODO add more Types

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    type: Mapped[NotifcationType] = mapped_column(
        String(50),
        nullable=False,
    )            # deployment_complete, strategy_shared, etc.

    title: Mapped[str] = mapped_column(
        String(50),
        nullable = False,
    )

    message: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=False,
    )      # related IDs, links

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )  # null = unread

    created_at: Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )