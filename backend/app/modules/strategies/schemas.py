
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class StrategyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class StrategyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class Strategy(BaseModel):
    id: UUID
    owner_id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    created_at: datetime
    archived_at: datetime | None = None

    model_config = {"from_attributes": True}


# Strategy is seperate from Strategy Version for a couple reasons:
# 1. A strategy's name and description can change in isolation.
# 2. This can represent a row in a different database table.


class StrategyVersionCreate(BaseModel):
    commit_hash: str = Field(min_length=1)
    entrypoint: str = Field(min_length=1)
    artifact_path: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)


class StrategyVersion(BaseModel):
    id: UUID
    strategy_id: UUID
    commit_hash: str
    entrypoint: str
    artifact_path: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = {"from_attributes": True}
