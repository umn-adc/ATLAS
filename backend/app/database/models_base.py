"""Base class for SQLAlchemy models. Separate file to avoid circular imports with Alembic."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models. Define your models inheriting from this."""
