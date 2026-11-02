"""Logs router"""

from datetime import datetime
from typing import Annotated
from uuid import UUID


from fastapi import APIRouter, Depends, status

from app.modules.audit_logs.dependencies import get_audit_log_service, get_current_user_id
from app.modules.audit_logs.schemas import AuditEvent
from app.modules.audit_logs.service import AuditService

router = APIRouter()

@router.get(
    "/api/audit-logs",
    response_model=[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_logs(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[AuditService, Depends(get_audit_log_service)],
    before_datetime: datetime | None = None
):
    return await service.get_logs(user_id, before_datetime)

@router.get(
    "/api/audit-logs/{resource_type}/{resource_id}",
    response_model=[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_resource_logs(
    resource_type: str,
    resource_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[AuditService, Depends(get_audit_log_service)],
    before_datetime: datetime | None = None

):
    return await service.get_resource_logs(resource_type, resource_id, user_id, before_datetime)