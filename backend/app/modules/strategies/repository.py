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
        strategy = Strategy(owner_id=owner_id, name=name, description=description)
        self.session.add(strategy)

        # save changes on current transaction
        # opted for flush() and refresh() instead of commit() #TODO: need to implement commit calls elsewhere
        # keeps changes within an open transaction, allowing for further calls and/or rollback if necessary
        await self.session.flush()
        await self.session.refresh(strategy)

        return strategy

    async def get_by_id(self, strategy_id: UUID) -> Strategy | None:
        """Return a strategy by ID, or None if not found."""
        
        return await self.session.get(Strategy, strategy_id)

    async def list_by_owner(self, owner_id: UUID, include_archived: bool = False) -> list[Strategy]:
        """Return all strategies for an owner, optionally including archived, unordered."""
        stmt = select(Strategy).where(Strategy.owner_id == owner_id) # get all strategies by owner id
        
        if not include_archived: # check if archived strategies should be excluded
            stmt = stmt.where(Strategy.archived_at.is_(None))
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, strategy: Strategy) -> Strategy:
        """Persist changes to an existing strategy."""
        self.session.add(strategy)
        await self.session.flush()
        await self.session.refresh(strategy)
        return strategy



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
        """Insert a new strategy version and return it."""
        version = StrategyVersion(
            strategy_id=strategy_id,
            commit_hash=commit_hash,
            entrypoint=entrypoint,
            artifact_path=artifact_path,
            parameters=parameters,
        )
        self.session.add(version)
        await self.session.flush()
        await self.session.refresh(version)
        return version


    async def list_by_strategy(self, strategy_id: UUID) -> list[StrategyVersion]:
        """Return all versions for a strategy, ordered by created_at desc."""
        stmt = (
            select(StrategyVersion)
            .where(StrategyVersion.strategy_id == strategy_id)
            .order_by(StrategyVersion.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

        
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
