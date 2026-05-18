from fastapi import APIRouter, HTTPException
from ..models import JobResponse, JobStatus
from .. import jobs

router = APIRouter()


@router.get("/job/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse(job_id=job_id, **job)
