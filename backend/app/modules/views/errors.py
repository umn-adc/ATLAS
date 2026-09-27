"""Custom exceptions for views module."""

from uuid import UUID

from fastapi import HTTPException, status


class ViewNotFoundError(HTTPException):
    """Raised when view does not exist."""

    def __init__(self, view_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"View {view_id} not found",
        )


class ViewOwnershipError(HTTPException):
    """Raised when user doesn't own the view."""

    def __init__(self, view_id: UUID):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User doesn't own view {view_id}",
        )
