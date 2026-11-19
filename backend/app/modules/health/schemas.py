from enum import StrEnum, auto

from pydantic import BaseModel

class Database_Status(StrEnum):
    OK = "ok"
    UNREACHABLE = "unreachable"

class HealthResponse(BaseModel):
    version: str
    database_status: Database_Status