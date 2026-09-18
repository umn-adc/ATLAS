"""Views' Module's implementation of the Service-Repository pattern"""

from uuid import UUID

from app.modules.views.repository import ViewsRepository
from app.modules.views.schemas import ViewCreate, ViewResponse


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