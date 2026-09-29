"""Service layer for user business logic."""

from uuid import UUID

from app.modules.users.repository import UserRepository
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate, UserPasswordUpdate

import bcrypt

from sqlalchemy.exc import IntegrityError


class UserService:
    """
    Business logic layer for user operations.

    Orchestrates repository calls and enforces business rules.
    Handles password hashing, validation, and authorization checks.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, data: UserCreate) -> User:
        """
        Register a new user.

        Args:
            data: UserCreate schema containing username and plaintext password

        Returns:
            User: The created user model instance

        Raises:
            ValueError: If username is already taken

        Implementation:
            Check if username exists by querying repository.
            If taken, raise ValueError with descriptive message.
            Hash the plaintext password using a secure algorithm like bcrypt.
            Call repository create method with username and hashed password.
            Return the created user.
        """
        password = data.password.encode("utf-8")
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            return await self.repository.create(data.username, hashed_pw)
        except IntegrityError:
            raise ValueError("Username is already taken")

    async def get_user(self, user_id: UUID) -> User:
        """
        Fetch a single user by ID.

        Args:
            user_id: UUID of the user to retrieve

        Returns:
            User: The user model instance

        Raises:
            ValueError: If user does not exist

        Implementation:
            Query repository for user by ID.
            If None returned, raise ValueError.
            Return the user.
        """
        raise NotImplementedError

    async def get_user_by_username(self, username: str) -> User:
        """
        Fetch user by username. Exposed for other modules that need user lookup.

        Args:
            username: Username string

        Returns:
            User: The user model instance

        Raises:
            ValueError: If user does not exist

        Implementation:
            Query repository for user by username.
            If None returned, raise ValueError.
            Return the user.
        """
        raise NotImplementedError

    async def list_users(self, include_inactive: bool = False) -> list[User]:
        """
        List all users. Typically an admin-only operation.

        Args:
            include_inactive: Whether to include deactivated users

        Returns:
            list[User]: All matching user instances

        Implementation:
            Call repository list_all with the include_inactive flag.
            Return the result directly.
        """
        raise NotImplementedError

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        """
        Update user profile or status fields.

        Args:
            user_id: UUID of user to update
            data: UserUpdate schema with optional fields to change

        Returns:
            User: The updated user model instance

        Raises:
            ValueError: If user does not exist
            ValueError: If new username is already taken by another user

        Implementation:
            Fetch user from repository by ID, raise if not found.
            If username is being changed, check it's not taken by another user.
            Apply only the non-None fields from data to the user model.
            Call repository update and return the result.
        """
        raise NotImplementedError

    async def update_password(self, user_id: UUID, data: UserPasswordUpdate) -> User:
        """
        Change a user's password. User must provide current password.

        Args:
            user_id: UUID of user changing password
            data: UserPasswordUpdate with current and new passwords

        Returns:
            User: The updated user model instance

        Raises:
            ValueError: If user does not exist
            ValueError: If current password is incorrect

        Implementation:
            Fetch user from repository by ID, raise if not found.
            Verify current_password matches the stored password_hash.
            If mismatch, raise ValueError.
            Hash the new password and update password_hash field.
            Call repository update and return the result.
        """
        raise NotImplementedError

    async def delete_user(self, user_id: UUID) -> None:
        """
        Permanently delete a user. Admin operation.

        Args:
            user_id: UUID of user to delete

        Returns:
            None

        Raises:
            ValueError: If user does not exist

        Implementation:
            Fetch user from repository by ID, raise if not found.
            Call repository delete method.
        """
        raise NotImplementedError

    async def deactivate_user(self, user_id: UUID) -> User:
        """
        Soft delete by setting is_active to False. Admin operation.

        Args:
            user_id: UUID of user to deactivate

        Returns:
            User: The updated user model instance

        Raises:
            ValueError: If user does not exist

        Implementation:
            Fetch user from repository by ID, raise if not found.
            Set is_active to False on the user model.
            Call repository update and return the result.
        """
        raise NotImplementedError
