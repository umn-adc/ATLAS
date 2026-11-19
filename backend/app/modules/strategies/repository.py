from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.strategies.models import Strategy, StrategyVersion


class StrategyRepository:
    """Database operations for strategies."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, owner_id: UUID, name: str, description: str | None) -> Strategy:
        """Insert a new strategy and return it."""
        raise NotImplementedError

    async def get_by_id(self, strategy_id: UUID) -> Strategy | None:
        """Return a strategy by ID, or None if not found."""
        raise NotImplementedError

    async def list_by_owner(self, owner_id: UUID, include_archived: bool = False) -> list[Strategy]:
        """Return all strategies for an owner, optionally including archived."""
        raise NotImplementedError

    async def update(self, strategy: Strategy) -> Strategy:
        """Persist changes to an existing strategy."""
        raise NotImplementedError


class StrategyVersionRepository:
    """Database operations for strategy versions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        strategy_id: UUID,
        commit_hash: str,
        entrypoint: str,
        artifact_path: str,
        parameters: dict,
    ) -> StrategyVersion:
        version = StrategyVersion(
            strategy_id=strategy_id,
            commit_hash=commit_hash,
            entrypoint=entrypoint,
            artifact_path=artifact_path,
            parameters=parameters,
            created_at=datetime.now(),
        )
        self.session.add(version)
        await self.session.commit()
        await self.session.refresh(version)
        return version

    async def list_by_strategy(self, strategy_id: UUID) -> list[StrategyVersion]:
        statement = select(StrategyVersion).where(StrategyVersion.strategy_id == strategy_id)

        result = await self.session.execute(statement)

        return list(result.scalars().all())
