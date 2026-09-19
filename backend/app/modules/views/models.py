"""SQLAlchemy models for views module."""

import uuid
from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models_base import Base


class View(Base):
    __tablename__ = "views"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(String(36), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    layout: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
