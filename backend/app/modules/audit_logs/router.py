"""Logs router"""

from datetime import datetime
from typing import Annotated
from uuid import UUID


from fastapi import APIRouter, Depends, status

from app.modules.audit_logs.dependencies import get_audit_log_service, get_current_user_id
from app.modules.audit_logs.schemas import AuditEvent, AuditEventCreate, WarningLevel
from app.modules.audit_logs.service import AuditService

router = APIRouter(
     prefix="/api/audit-logs"
 )

@router.post(
    "",
    response_model=AuditEvent,
    status_code=status.HTTP_201_CREATED,
)
async def create_logs(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[AuditService, Depends(get_audit_log_service)],
    data: AuditEventCreate,
    warning: WarningLevel = WarningLevel.NONE,
    details: dict | None = None
):
    return await service.log_action(user_id, data, details, warning)


@router.get(
    "/{log_id}",
    response_model=AuditEvent,
    status_code=status.HTTP_200_OK,
)
async def get_log_by_id(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    log_id: UUID,
    service: Annotated[AuditService, Depends(get_audit_log_service)],
):
    return await service.get_log_by_id(log_id=log_id)


@router.get(
    "/actor/{actor_id}",
    response_model=list[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_logs_by_actor(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    actor_id: UUID,
    service: Annotated[AuditService, Depends(get_audit_log_service)]
    #before_datetime: datetime | None = None
):
    return await service.get_logs_by_actor(actor_id=actor_id)


@router.get(
    "/target/{target_id}",
    response_model=list[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_target_resource_logs(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    target_id: UUID,
    service: Annotated[AuditService, Depends(get_audit_log_service)],
    #before_datetime: datetime | None = None
):
    return await service.get_logs_by_target(target_id=target_id)


@router.get(
    "/warning/{warning_level}",
    response_model=list[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_logs_by_warning(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    warning_level: WarningLevel,
    service: Annotated[AuditService, Depends(get_audit_log_service)]
    #before_datetime: datetime | None = None
):
    return await service.get_logs_by_warning(warning_level=warning_level)


@router.get(
    "/action/{action}",
    response_model=list[AuditEvent],
    status_code=status.HTTP_200_OK,
)
async def get_logs_by_action(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    action: str,
    service: Annotated[AuditService, Depends(get_audit_log_service)]
    #before_datetime: datetime | None = None
):
    return await service.get_logs_by_action(action=action)