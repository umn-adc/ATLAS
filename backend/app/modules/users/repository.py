"""Repository layer for user database operations."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.users.models import User

from sqlalchemy.exc import IntegrityError


class UserRepository:
    """
    Data access layer for User model.

    All database operations go here. No business logic.
    Service layer calls these methods.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, username: str, password_hash: str) -> User:
        """
        Insert new user into database.

        Args:
            username: Unique username string
            password_hash: Already-hashed password from service layer

        Returns:
            User: The created user model instance with id and timestamps populated

        Raises:
            IntegrityError: If username already exists (unique constraint)

        Implementation:
            Create a new User model instance with the provided fields.
            Add it to the session, commit, and refresh to get database-generated values.
            Return the user instance.
        """

        user = User(
            username=username,
            password_hash=password_hash,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Fetch user by primary key.

        Args:
            user_id: UUID of the user to find

        Returns:
            User | None: User model if found, None if no match

        Implementation:
            Build a select statement filtering by id.
            Execute and return the scalar result.
        """
        raise NotImplementedError

    async def get_by_username(self, username: str) -> User | None:
        """
        Fetch user by username. Used for login and uniqueness checks.

        Args:
            username: Username string to search for

        Returns:
            User | None: User model if found, None if no match

        Implementation:
            Build a select statement filtering by username.
            Execute and return the scalar result.
        """
        raise NotImplementedError

    async def list_all(self, include_inactive: bool = False) -> list[User]:
        """
        Fetch all users from database.

        Args:
            include_inactive: If False, filter out users where is_active=False

        Returns:
            list[User]: List of user model instances

        Implementation:
            Build a select statement for all users.
            If include_inactive is False, add a where clause for is_active=True.
            Execute and return all results as a list.
        """
        raise NotImplementedError

    async def update(self, user: User) -> User:
        """
        Persist changes to an existing user.

        Args:
            user: User model instance with modified fields

        Returns:
            User: The same user instance with updated_at refreshed

        Implementation:
            Set updated_at to current timestamp.
            Add the user to session, commit, and refresh.
            Return the updated user.
        """
        raise NotImplementedError

    async def delete(self, user: User) -> None:
        """
        Hard delete user from database.

        Args:
            user: User model instance to remove

        Returns:
            None

        Implementation:
            Delete the user from session and commit.
        """
        raise NotImplementedError
