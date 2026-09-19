"""Views router for dashboard layout management."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.views.dependencies import get_current_user_id, get_views_service
from app.modules.views.schemas import ViewCreate, ViewResponse
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
