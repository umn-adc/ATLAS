"""Logs router"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.audit_logs.dependencies import get_audit_log_service, get_current_user_id
from app.modules.audit_logs.schemas import Audit_Log
from app.modules.audit_logs.service import AuditService


router = APIRouter()

#Need from other files
#-Audit_Log class in schemas.py
#-get_logs/get_resource_logs classes inside of AuditService Class in service.py
#-get_audit_log_service function and get_current_user_id in dependencies.py

@router.get(
    "/api/audit-logs",
    response_model=Audit_Log,
    status_code=status.HTTP_200_OK,
)
async def get_logs(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[AuditService, Depends(get_audit_log_service)],
):
    return await service.get_logs(user_id)

@router.get(
    "/api/audit-logs/{resource_type}/{resource_id}",
    response_model=Audit_Log,
    status_code=status.HTTP_200_OK,
)
async def get_resource_logs(
    resource_type: PLACEHOLDER,
    resource_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[AuditService, Depends(get_audit_log_service)],
):
    return await service.get_resource_logs(resource_type, resource_id, user_id)