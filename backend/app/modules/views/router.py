"""Views router for dashboard layout management."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.views.dependencies import get_current_user_id, get_views_service
from app.modules.views.schemas import ViewCreate, ViewResponse, ViewUpdate
from app.modules.views.service import ViewsService

router = APIRouter()


@router.post(
    "/",
    response_model=ViewResponse,  # The Pydantic type to put the response in
    status_code=status.HTTP_201_CREATED,
)
async def create_view(
    data: ViewCreate,
    # We need to get a ViewsService which holds all the business logic
    # Depends() in FastAPI is for Dependency Injection
    # It tells FastAPI to call get_views_service (the service creator) and return it to us
    service: Annotated[ViewsService, Depends(get_views_service)],
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
):
    return await service.create(data, owner_id)


@router.get(
    "/",
    response_model=list[ViewResponse],
    status_code=status.HTTP_200_OK,
)
async def get_views(
    service: Annotated[ViewsService, Depends(get_views_service)],
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
):
    return await service.get_all(owner_id)


@router.get(
    "/{view_id}",
    response_model=ViewResponse,
    status_code=status.HTTP_200_OK,
)
async def get_view(
    view_id: UUID,
    service: Annotated[ViewsService, Depends(get_views_service)],
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
):
    return await service.get(view_id, owner_id)


@router.patch(
    "/{view_id}",
    response_model=ViewResponse,
    status_code=status.HTTP_200_OK,
)
async def update_view(
    view_id: UUID,
    data: ViewUpdate,
    service: Annotated[ViewsService, Depends(get_views_service)],
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
):
    return await service.update(view_id, owner_id, data)


@router.delete(
    "/{view_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_view(
    view_id: UUID,
    service: Annotated[ViewsService, Depends(get_views_service)],
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
):
    await service.delete(view_id, owner_id)
