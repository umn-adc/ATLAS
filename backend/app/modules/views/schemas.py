from pydantic import BaseModel, Field
from uuid import UUID
from typing import Any

class CardConfig(BaseModel):
    id: str


class ViewCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    layout: dict = {}


class ViewUpdate(BaseModel):
    name: str | None = None
    layout: dict | None = None


class ViewResponse(BaseModel):
    id: int
    name: str
    layout: dict