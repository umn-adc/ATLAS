from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.modules.audit_logs.repository import AuditRepository
from app.modules.audit_logs.service import AuditService

def get_audit_log_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuditRepository:
    return AuditRepository(db)

def get_audit_log_service(
    repository: Annotated[AuditRepository, Depends(get_audit_log_repository)]
) -> AuditService:
    return AuditService(repository)

def get_current_user_id() -> UUID:
    # TODO: replace with the real user from the auth token
    raise NotImplementedError