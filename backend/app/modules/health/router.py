"""Health router for health endpoints"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.modules.health.schemas import HealthResponse, Database_Status

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request, db: AsyncSession = Depends(get_db)):
    database_status = Database_Status.OK
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        database_status = Database_Status.UNREACHABLE

    return HealthResponse(
            version=request.app.version,
            database_status=database_status,
        )