from collections.abc import AsyncGenerator
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    # Default: SQLite file in data/ directory (self-hosted friendly)
    database_url: str = "sqlite+aiosqlite:///./data/atlas.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Ensure data directory exists for SQLite
if settings.database_url.startswith("sqlite"):
    db_path = settings.database_url.replace("sqlite+aiosqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

# engine is the connection pool
# and the entry point for all DB operations
# A connection pool is between the application and database,
# and it makes sure you don't overload the DB.
# singleton, one per app
engine = create_async_engine(
    settings.database_url,
    # SQLite needs this for async
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# async session factory
# sessions are units of works, they track changes to objects, and commit or rollback as a batch
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all ORM models. Define your models inheriting from this."""



async def init_db() -> None:
    """Create all tables defined by models inherting from base. For production, use Alembic migrations instead."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency that yields a database session."""
    async with async_session() as session:
        yield session
