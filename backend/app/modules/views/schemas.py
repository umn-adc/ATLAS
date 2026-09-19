"""Schemas for views module."""

from typing import Any
from uuid import UUID

# with `Field`, you can specify defaults and rules for values
from pydantic import BaseModel, Field


class CardConfig(BaseModel):
    id: UUID
    type: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    w: int = Field(ge=0)
    h: int = Field(ge=0)
    config: dict[str, Any] = {}


class ViewLayout(BaseModel):
    cards: list[CardConfig] = []


class ViewCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    layout: ViewLayout = Field(default_factory=ViewLayout)


class ViewUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    layout: dict | None = None


class ViewResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    layout: ViewLayout

    # allows us to read data from attributes from objects like a SQLAlchemy object
    # This converts a custom object into a Pydantic response it can parse
    model_config = {"from_attributes": True}
