from datetime import datetime
from typing import Any
from uuid import UUID
from enum import Enum, IntEnum

from pydantic import BaseModel, Field, ConfigDict

# outcome of an audit log event
class Outcome(str, Enum): # Enum forces Outcome to only be one of the 3 possible values listed
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"

# degree of severity/attention needed
class WarningLevel(IntEnum):
    NONE = 0
    MINOR = 1
    URGENT = 2

# a singular audit log event
class AuditEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True) # 2nd field tells Pydantic to reject any input fields that weren't declared
    id: UUID # unique id
    action: str # what
    actor_id: UUID # who
    actor_type: type # what kind of entity performed the action (e.g. user, service, system)
    target: UUID | None = None # to what
    target_type: str | None = None # type of target (e.g. invoice, user)
    outcome: Outcome
    timestamp: datetime # when
    details: dict | None = None # JSON - old/new values
    warning_level: WarningLevel # degree of severity/attention needed
    schema_version: int = 1 # records iterations of schema

# class to create an audit event
class AuditEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid") # 2nd field tells Pydantic to reject any input fields that weren't declared

    action: str
    target: UUID | None = None # to what
    target_type: str | None = None # type of target (e.g. invoice, user)
    outcome: Outcome