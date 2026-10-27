from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import init_db, settings
from app.modules.strategies.router import router as strategy_router
from app.modules.views.router import router as views_router


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

    # Let the frontend call the API from the browser.
    # Methods and headers must be opened up, or preflight for JSON POSTs fails.
    # If allow_credentials is turned on later, never put "*" in cors_origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
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

    @app.get("/api/health", tags=["Health"])
    async def health():
        return {"status": "ok"}

    return app


# ---

app = create_app()
