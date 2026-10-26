from datetime import datetime
from typing import Any
from uuid import UUID
from enum import Enum, IntEnum

from pydantic import BaseModel, Field

# the actor of an audit log event
class Actor(BaseModel):
    model_config = ConfigDict(frozen=True) # enforces unchangeable records
    id: str # what specific entity performed the action
    type: str # what kind of entity performed the action (e.g. user, service, system)
    ip_address: str | None = None
    # user_agent: str | None = None # stores HTTP User-Agent header from request that triggered action
    
# target of an audit log event
class Target(BaseModel):
    model_config = ConfigDict(frozen=True) # enforces unchangeable records
    type: str # type of target (e.g. invoice, user)
    id: str

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
    model_config = ConfigDict(frozen=True, extra="forbid") # 2nd field tells Pydantic to reject any input fields that weren't declared
    id: UUID # unique id
    action: str # what
    actor: Actor # who
    target: Target | None = None # to what
    outcome: Outcome
    timestamp: datetime # when
    details: dict # JSON - old/new values
    warning_level: WarningLevel # degree of severity/attention needed
    schema_version: int = 1 # records iterations of schema

# class to create an audit event
class AuditEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid") # 2nd field tells Pydantic to reject any input fields that weren't declared

    action: str
    actor: Actor
    target: Target | None = None
    outcome: Outcome