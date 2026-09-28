"""Pydantic schemas for user request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Schema for updating user profile/status. All fields optional."""

    username: str | None = Field(default=None, min_length=3, max_length=16)
    is_active: bool | None = None
    is_admin: bool | None = None


class UserPasswordUpdate(BaseModel):
    """Schema for changing password."""

    current_password: str
    new_password: str = Field(min_length=8)


class User(BaseModel):
    """Response schema for user data. Excludes password_hash."""

    id: UUID
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
