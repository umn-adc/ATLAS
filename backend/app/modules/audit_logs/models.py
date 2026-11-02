from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, String, func, Enum, Index, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models_base import Base
from app.modules.audit_logs.schemas import Outcome

ACTION_MAX_LEN = 50
ID_MAX_LEN = 100
TYPE_MAX_LEN = 50

class AuditEvent(Base):
    __tablename__ = "audit_log"

    id: Mapped[UUID] = mapped_column(
        primary_key = True,
        default = uuid4,  # create the uuid
    )

    # should be a short label of what happened
    # convention: resource.verb (e.g. user.login)
    action: Mapped[str] = mapped_column(
        String(ACTION_MAX_LEN),
        nullable = False,
        index = True # improves lookup and querying table, esp at large scale
    )

    # separated for easier usage
    actor_id: Mapped[str] = mapped_column(String(ID_MAX_LEN), nullable=False)
    actor_type: Mapped[str] = mapped_column(String(TYPE_MAX_LEN), nullable=False)

    # separated for easier usage
    target_id: Mapped[str | None] = mapped_column(String(ID_MAX_LEN))
    target_type: Mapped[str | None] = mapped_column(String(TYPE_MAX_LEN))

    # success, failure, or denied
    # enforced by enum
    outcome: Mapped[Outcome] = mapped_column(
        Enum(
            Outcome,
            native_enum = False, # stores value as a plain string column, easier to migrate
            values_callable = lambda e: [m.value for m in e], # store "success", not "SUCCESS"
            create_constraint = True # have the database reject unknown values
        ),
        nullable = False
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default=lambda: datetime.now(timezone.utc),
        server_default = func.now(),
        nullable = False
    )

    # json file that contains what was changed, along with old and new values if applicable
    # empty for many events
    details: Mapped[dict[str, Any] | None] = mapped_column(
        JSON
    )

    # 0 = no attention needed, 1 = slight issue, 2 = immediate attention
    warning_level: Mapped[int] = mapped_column(
        SmallInteger,
        default = 0,
        nullable = False
    )

    schema_version: Mapped[int] = mapped_column(
        SmallInteger,
        default = 1,
        nullable = False
    )