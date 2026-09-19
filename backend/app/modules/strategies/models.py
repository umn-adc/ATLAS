from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models_base import Base


class Strategy(Base):
    __tablename__ = "strategies"

    # A mapped attribute is a Python object variable that SQLAlchemy connects
    # to a database column. We use Mapped and mapped_column to map them
    # A mapped attribute allows u to interact with the DB row as if it was a Python obj
    #
    # strategy = await session.get(Strategy, some_id)
    # print(strategy.name)
    #
    # Read as: Create a column called `id` in the `strategies` table.
    # Store a UUID inside it and generate a UUID automatically when default inserting
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,  # create the uuid
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class StrategyVersion(Base):
    __tablename__ = "strategy_versions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    strategy_id: Mapped[UUID] = mapped_column(
        ForeignKey("strategies.id"),
        nullable=False,
        index=True,
    )

    commit_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    entrypoint: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    artifact_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    parameters: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
