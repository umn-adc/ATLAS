"""Views' Module's implementation of the Service-Repository pattern"""

from uuid import UUID

from app.modules.views.errors import ViewNotFoundError, ViewOwnershipError
from app.modules.views.repository import ViewsRepository
from app.modules.views.schemas import ViewCreate, ViewResponse, ViewUpdate


class ViewsService:
    # Creates a ViewsService given a repository
    def __init__(self, repository: ViewsRepository):
        self.repository = repository

    # Router calls this.
    # This (Service Layer) calls the repository
    # Repository will handle querying the database
    # When repository returns the service layer returns it aswell
    # Once returned to the router, the router will serialize it as the HTTP response
    async def create(self, data: ViewCreate, owner_id: UUID) -> ViewResponse:
        view = await self.repository.create(
            owner_id=owner_id,
            name=data.name,
            # Turns ViewCreate.ViewLayout Pydantic object into JSON
            # It does this so it can store a JSONB (json blob) on the database
            layout=data.layout.model_dump(mode="json"),
        )

        return ViewResponse.model_validate(view)

    async def get_all(self, owner_id: UUID) -> list[ViewResponse]:
        # There will never be too many views, no need for streaming it
        views = await self.repository.get_all(owner_id=owner_id)

        return [ViewResponse.model_validate(view) for view in views]

    async def get(self, view_id: UUID, owner_id: UUID) -> ViewResponse:
        view = await self.repository.get_by_id(view_id)

        if view is None:
            raise ViewNotFoundError(view_id)

        if view.owner_id != str(owner_id):
            raise ViewOwnershipError(view_id)

        return ViewResponse.model_validate(view)

    async def update(self, view_id: UUID, owner_id: UUID, data: ViewUpdate) -> ViewResponse:
        view = await self.repository.get_by_id(view_id)

        if view is None:
            raise ViewNotFoundError(view_id)

        if view.owner_id != str(owner_id):
            raise ViewOwnershipError(view_id)

        if data.name is not None:
            view.name = data.name
        if data.layout is not None:
            view.layout = data.layout

        view = await self.repository.update(view)
        return ViewResponse.model_validate(view)

    async def delete(self, view_id: UUID, owner_id: UUID) -> None:
        view = await self.repository.get_by_id(view_id)

        if view is None:
            raise ViewNotFoundError(view_id)

        if view.owner_id != str(owner_id):
            raise ViewOwnershipError(view_id)

        await self.repository.delete(view)
