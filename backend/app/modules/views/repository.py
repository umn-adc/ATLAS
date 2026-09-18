from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel


class View(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    layout: dict[str, Any]


class ViewsRepository:
    def __init__(self):
        self.views: dict[UUID, View] = {}

    async def create(
        self,
        owner_id: UUID,
        name: str,
        layout: dict[str, Any],
    ) -> View:
        view = View(
            id=uuid4(),
            owner_id=owner_id,
            name=name,
            layout=layout,
        )

        self.views[view.id] = view
        return view