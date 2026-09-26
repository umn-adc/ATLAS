from uuid import UUID

from app.modules.strategies.schemas import (
    Strategy,
    StrategyCreate,
    StrategyUpdate,
    StrategyVersion,
    StrategyVersionCreate,
)

from app.modules.views.repository import ViewsRepository


class StrategyService:
    """Manages strategy lifecycle and versioning."""

    def __init__(self, repository):  # potential issue?? should we be using views??
        self.repository = repository

    # BEGINNER TASKS - Service methods only (no repository/API)

    # beginner

    def get_strategy(self, strategy_id: UUID, user_id: UUID) -> Strategy:
        """Return a strategy by ID if the user owns it.
        Raises ValueError if strategy not found or user doesn't own it.
        """

        strategy = self.repository.get_by_id(strategy_id)

        if strategy == None:
            raise ValueError("Strategy not found")

        if strategy.owner_id != user_id:
            raise ValueError("User doesn't own this strategy")

        return strategy

    # beginner
    def list_user_strategies(self, user_id: UUID) -> list[Strategy]:
        """Return all non-archived strategies owned by the user."""
        raise NotImplementedError

    # beginner
    def update_strategy(self, strategy_id: UUID, user_id: UUID, data: StrategyUpdate) -> Strategy:
        """Update a strategy's name or description if the user owns it.

        Raises ValueError if strategy not found or user doesn't own it.
        """
        raise NotImplementedError

    # beginner
    def archive_strategy(self, strategy_id: UUID, user_id: UUID) -> Strategy:
        """Soft-delete a strategy by setting archived_at if the user owns it.

        Raises ValueError if strategy not found or user doesn't own it.
        """
        raise NotImplementedError

    # ADVANCED TASKS - implement repository + service + router

    def create_strategy(self, user_id: UUID, data: StrategyCreate) -> Strategy:
        """Create a new strategy owned by the user."""
        raise NotImplementedError

    def create_version(
        self, strategy_id: UUID, user_id: UUID, data: StrategyVersionCreate
    ) -> StrategyVersion:
        """Register a new immutable version for a strategy.

        Raises ValueError if strategy not found or user doesn't own it.
        """
        raise NotImplementedError

    def list_versions(self, strategy_id: UUID, user_id: UUID) -> list[StrategyVersion]:
        """Return all versions for a strategy if the user owns it.

        Raises ValueError if strategy not found or user doesn't own it.
        """
        raise NotImplementedError
