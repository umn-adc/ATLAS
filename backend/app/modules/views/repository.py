"""Repository layer for views - handles database queries."""

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.views.models import View


class ViewsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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

        self.session.add(view)  # Place an object into this object
        await self.session.commit()  # Commit the current transaction in progress
        await self.session.refresh(view)
        return view

    async def get_all(self, owner_id: UUID) -> list[View]:
        # Build the SQL statement with SQLAlchemy Python
        # You can literally build the sql's clauses (select, where) with it
        statement = select(View).where(View.owner_id == owner_id)

        # Execute the SQL statement and save result
        result = await self.session.execute(statement)

        # Result is like this conceptually, before scalars():
        # [(View(id=1),), (View(id=2),)]
        # .scalars() extracts the objects from those rows:
        # View(id=1), View(id=2)
        # .all() collects all the extracted objects into a sequence
        # [View(id=1), View(id=2)]
        return list(result.scalars().all())
