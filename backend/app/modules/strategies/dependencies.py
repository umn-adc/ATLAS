from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.modules.strategies.repository import StrategyRepository
from app.modules.strategies.service import StrategyService

def get_strategies_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StrategyRepository:
    return StrategyRepository(db)

def get_strategies_service(
    repository: Annotated[StrategyRepository, Depends(get_strategies_repository)]
) -> StrategyService:
    return StrategyService(repository)

def get_current_user_id() -> UUID:
    # TODO: replace with the real user from the auth token
    return _PLACEHOLDER_USER_ID