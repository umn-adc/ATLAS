"""Custom exceptions for audit logs module."""

from uuid import UUID

from fastapi import HTTPException, status


class LogsNotFoundError(HTTPException):
    """Raised when an audit log entry can not be found."""

    def __init__(self, log_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit log entry with ID '{log_id}' was not found.",
        )


class AuditAccessDeniedError(HTTPException):
    """Raised when a user lacks permission to view audit logs."""

    def __init__(self, user_id: UUID, resource_id: UUID):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User '{user_id}' does not have permission to access resource '{resource_id}'.",
        )

# class *ErrorName*(HTTPException):
#     """*Error Discription*"""

#     def __init__(self, *What vars are needed*):
#         super().__init__(
#             status_code=status.*HTTP Error Code*,
#             detail=f"*String Output*",
#         )