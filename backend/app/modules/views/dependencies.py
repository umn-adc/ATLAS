"""Dependency providers for the views module."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.views.repository import ViewsRepository
from app.modules.views.service import ViewsService

# The repository is in-memory for now, so it must be a single shared instance.
# Creating one per request would lose every view as soon as the request ends.
_views_repository = ViewsRepository()

# Placeholder until authentication exists. Every view is owned by this user.
_PLACEHOLDER_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def get_views_repository() -> ViewsRepository:
    return _views_repository


def get_views_service(
    repository: Annotated[ViewsRepository, Depends(get_views_repository)],
) -> ViewsService:
    return ViewsService(repository)


def get_current_user_id() -> UUID:
    # TODO: replace with the real user from the auth token
    return _PLACEHOLDER_USER_ID
