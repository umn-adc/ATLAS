"""Repository layer for views - handles database queries."""

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.views.models import View


class ViewsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        owner_id: UUID,
        name: str,
        layout: dict[str, Any],
    ) -> View:
        view = View(
            owner_id=str(owner_id),
            name=name,
            layout=layout,
        )

        self.db.add(view)  # Place an object into this object
        await self.db.commit()  # Commit the current transaction in progress
        await self.db.refresh(view)
        return view
