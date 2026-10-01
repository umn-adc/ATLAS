"""Users router for user management endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.users.dependencies import get_users_service
from app.modules.users.schemas import UserCreate, User, UserUpdate, UserPasswordUpdate
from app.modules.users.service import UserService

router = APIRouter()


@router.post(
    "/users",
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
    try:
        return await service.create_user(data)
    except ValueError as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail =str(e))


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
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =str(e))


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
    try:
        return await service.update_user(user_id, data)
    except ValueError as e:
        detail = str(e)
        status_code = (
            status.HTTP_409_CONFLICT
            if "already taken" in detail
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=detail)


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
    try:
        await service.delete_user(user_id)
    except ValueError as e:
        raise HTTTPException(status_code=status.HTTP_404_NOT_FOUND, detial=str(e))


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
    try:
        return await service.deactivate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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
    try:
        return await service.update_password(user_id, data)
    except ValueError as e:
        detail = str(e)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "icorrect" in detail
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail =detail)
