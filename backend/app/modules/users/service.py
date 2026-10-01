"""Service layer for user business logic."""

from uuid import UUID

from app.modules.users.repository import UserRepository
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate, UserPasswordUpdate


class UserService:
    """
    Business logic layer for user operations.

    Orchestrates repository calls and enforces business rules.
    Handles password hashing, validation, and authorization checks.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository
    def __hash_password(self,password: str) -> str:
        """Hash a plaintext password"""
        return pwd_context.hash(password)
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """verify a plaintext password against a hash"""
        return pwd_context.verify(plain_password, hashed_password)

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
        existing = await self.repository.get_by_username(data.username)
        if existing:
            raise ValueError("Username is already taken.")
        
        hashed_password = self.__hash_password(data.password)
        return await self.repository.create(
            username=data.username,
            password_hash=hashed_password
        )

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
        user = await self.repository.get_by_username(username)
        if not user:
            raise ValueError("User not found.")
        return user 

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
        user = await self.repository.get_by_username(username)
        if not user:
            raise ValueError("User not found.")
        return user

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
        return await self.repository.list_all(include_inactive=include_inactive)

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
        User = await self.get_user(user_id)

        update_data = data.model_dump(exclude_unset=True)
        if "username" in update_data and update_data["username"] != user.username:
            existing = await self.repository.get_by_username(update_data["username"])
            if existing:
                raise ValueError("Username is already taken")
        
        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.repository.update(user)

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
        user = await self.get_user(user_id)

        #verify current passw
        if not self._verify_password(data.current_password, user.password_hash):
            raise ValueError("Current password is incorrect.")

        #Hash new password and save
        user.password_hash = self.__hash_password(data.new_password)
        return await self.repository.update(user)

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
        user = await self.get_user(user_id)
        await self.repository.delete(user)

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
        user = await self.get_user(user_id)
        user.is_active = False
        return await self.repository.update(user)
