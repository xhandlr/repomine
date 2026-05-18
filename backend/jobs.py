import uuid
from .models import JobStatus

# In-memory store: job_id -> job data
_store: dict[str, dict] = {}


def create() -> str:
    job_id = str(uuid.uuid4())
    _store[job_id] = {"status": JobStatus.pending, "progress": 0, "result": None, "error": None}
    return job_id


def get(job_id: str) -> dict | None:
    return _store.get(job_id)


def update(job_id: str, **kwargs) -> None:
    if job_id in _store:
        _store[job_id].update(kwargs)
