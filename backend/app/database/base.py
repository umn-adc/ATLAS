import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models_base import Base


class Settings(BaseSettings):
    # Default: SQLite file in data/ directory (self-hosted friendly)
    database_url: str = "sqlite+aiosqlite:///./data/atlas.db"

    # Browser origins allowed to call the API. Default is the Vite dev server.
    # Override with a comma-separated env var, e.g.
    # CORS_ORIGINS=http://localhost:5173,https://atlas.example.com
    # NoDecode stops pydantic-settings from requiring JSON for list fields.
    cors_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, v: object) -> object:
        """Accept a comma-separated string or a JSON list from the env var."""
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                return json.loads(v)
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

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


async def init_db() -> None:
    """Create all tables defined by models inherting from base. For production, use Alembic migrations instead."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency that yields a database session."""
    async with async_session() as session:
        yield session
