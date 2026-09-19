"""Dependency providers for the views module."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.views.repository import ViewsRepository
from app.modules.views.service import ViewsService

# Placeholder until authentication exists
_PLACEHOLDER_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def get_views_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ViewsRepository:
    return ViewsRepository(db)


def get_views_service(
    repository: Annotated[ViewsRepository, Depends(get_views_repository)],
) -> ViewsService:
    return ViewsService(repository)


def get_current_user_id() -> UUID:
    # TODO: replace with the real user from the auth token
    return _PLACEHOLDER_USER_ID
