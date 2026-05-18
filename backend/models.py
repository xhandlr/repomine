from pydantic import BaseModel
from enum import Enum


class Framework(str, Enum):
    nestjs   = "nestjs"
    angular  = "angular"
    react    = "react"
    generic  = "generic"


class AnalyzeRequest(BaseModel):
    repo: str
    framework: Framework = Framework.generic


class JobStatus(str, Enum):
    pending   = "pending"
    running   = "running"
    completed = "completed"
    failed    = "failed"


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress: int = 0
    error: str | None = None
    result: dict | None = None
