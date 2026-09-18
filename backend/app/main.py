from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.strategies.router import router as strategy_router
from app.modules.views.router import router as views_router


# Use lifespan functions to run code at app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("ATLAS backend starting")

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

    @app.get("/health", tags=["Health"])
    async def health():
        return {"status": "ok"}

    return app


# ---

app = create_app()
