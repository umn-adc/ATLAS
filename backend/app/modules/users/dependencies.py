"""Dependency injection for users module."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_users_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    """
    Inject UserRepository with database session.

    Dependency chain: get_db -> UserRepository

    Returns:
        UserRepository: Instance bound to current request's db session
    """
    return UserRepository(db)


def get_users_service(
    repository: Annotated[UserRepository, Depends(get_users_repository)],
) -> UserService:
    """
    Inject UserService with repository.

    Dependency chain: get_db -> UserRepository -> UserService

    Returns:
        UserService: Instance ready for business logic operations
    """
    return UserService(repository)
