"""Custom exceptions for strategies module."""

from uuid import UUID

from fastapi import HTTPException, status


class SourceNotFoundError(HTTPException):
    """Raised when source path does not exist."""

    def __init__(self, path: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Source path does not exist: {path}",
        )


class ArtifactExistsError(HTTPException):
    """Raised when artifact already exists."""

    def __init__(self, strategy_id: UUID, version_id: UUID):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Artifact already exists for strategy {strategy_id} version {version_id}",
        )
