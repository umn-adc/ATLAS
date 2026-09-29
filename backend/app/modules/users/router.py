"""Users router for user management endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.users.dependencies import get_users_service
from app.modules.users.schemas import UserCreate, User, UserUpdate, UserPasswordUpdate
from app.modules.users.service import UserService

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Create a new user.

    Request body:
        UserCreate with username (3-16 chars) and password (8-128 chars)

    Returns:
        User: Created user data (excludes password_hash)
    """
    return await service.create_user(data)


@router.get(
    "/users",
    response_model=list[User],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    service: Annotated[UserService, Depends(get_users_service)],
    include_inactive: bool = False,
):
    """
    List all users.

    Query params:
        include_inactive: Include deactivated users (default False)

    Returns:
        list[User]: All matching users
    """
    return await service.list_users(include_inactive)


@router.get(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Get single user by ID.

    Path params:
        user_id: UUID of user

    Returns:
        User: User data

    Raises:
        404: User not found
    """
    return await service.get_user(user_id)


@router.patch(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Update user profile or status.

    Path params:
        user_id: UUID of user

    Request body:
        UserUpdate with optional username, is_active, is_admin

    Returns:
        User: Updated user data

    Raises:
        404: User not found
        409: Username already taken
    """
    return await service.update_user(user_id, data)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Permanently delete a user.

    Path params:
        user_id: UUID of user

    Returns:
        None (204 No Content)

    Raises:
        404: User not found
    """
    await service.delete_user(user_id)


@router.post(
    "/users/{user_id}/deactivate",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def deactivate_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Soft delete by setting is_active=False.

    Path params:
        user_id: UUID of user

    Returns:
        User: Updated user with is_active=False

    Raises:
        404: User not found
    """
    return await service.deactivate_user(user_id)


@router.post(
    "/users/{user_id}/password",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def update_password(
    user_id: UUID,
    data: UserPasswordUpdate,
    service: Annotated[UserService, Depends(get_users_service)],
):
    """
    Change user password.

    Path params:
        user_id: UUID of user

    Request body:
        UserPasswordUpdate with current_password and new_password

    Returns:
        User: Updated user data

    Raises:
        404: User not found
        400: Current password incorrect
    """
    return await service.update_password(user_id, data)
