from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.base import init_db
from app.modules.strategies.router import router as strategy_router
from app.modules.views.router import router as views_router
from app.modules.users.router import router as user_router


# Use lifespan function to run code at app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("ATLAS backend starting")
    await init_db()
    yield
    print("ATLAS backend stopping")


def create_app() -> FastAPI:
    app = FastAPI(
        title="ATLAS API",
        description="Backend API for the ATLAS trading platform.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(
        strategy_router,
        prefix="/api/strategies",
        tags=["Strategies"],
    )

    app.include_router(
        views_router,
        prefix="/api/views",
        tags=["Views"],
    )

    app.include_router(
        user_router,
        prefix="/api/users",
        tags=["Users"],
    )

    @app.get("/health", tags=["Health"])
    async def health():
        return {"status": "ok"}

    return app


# ---

app = create_app()
