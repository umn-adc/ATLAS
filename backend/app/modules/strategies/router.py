"""Strategies router for trading strategy management."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.strategies.dependencies import get_strategies_service, get_current_user_id
from app.modules.strategies.schemas import StrategyCreate, Strategy, StrategyUpdate, StrategyVersionCreate, StrategyVersion
from app.modules.strategies.service import StrategyService

router = APIRouter()

@router.post(
    "/strategies",
    response_model=Strategy,
    status_code=status.HTTP_201_CREATED,
)
async def create_strategy(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    data: StrategyCreate,
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.create_strategy(user_id, data)

@router.get(
    "/strategies",
    response_model=list[Strategy],
    status_code=status.HTTP_200_OK,
)
async def list_user_strategies(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return service.list_user_strategies(user_id)

@router.get(
    "/strategies{id}",
    response_model=Strategy,
    status_code=status.HTTP_200_OK,
)
async def get_strategy(
    strategy_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.get_strategy(strategy_id, user_id)

@router.patch(
    "/strategies{id}",
    response_model=Strategy,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_strategy(
    strategy_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    data: StrategyUpdate,
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.update_strategy(strategy_id, user_id, data)

@router.delete(
    "/strategies{id}",
    response_model=Strategy,
    status_code=status.HTTP_202_ACCEPTED,
)
async def archive_strategy(
    strategy_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.archive_strategy(strategy_id, user_id)

@router.post(
    "/strategies/{id}/versions",
    response_model=StrategyVersion,
    status_code=status.HTTP_201_CREATED,
)
async def create_version(
    strategy_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    data: StrategyVersionCreate,
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.create_version(strategy_id, user_id, data)

@router.get(
    "/strategies/{id}/versions",
    response_model=StrategyVersion,
    status_code=status.HTTP_200_OK,
)
async def list_versions(
    strategy_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[StrategyService, Depends(get_strategies_service)],
):
    return await service.list_versions(strategy_id, user_id)





