from fastapi import APIRouter, BackgroundTasks
from ..models import AnalyzeRequest, JobResponse, JobStatus
from .. import jobs
from core.git.runner import run_all

router = APIRouter()


def _run_analysis(job_id: str, repo: str) -> None:
    try:
        jobs.update(job_id, status=JobStatus.running, progress=10)
        result = run_all(repo)
        jobs.update(job_id, status=JobStatus.completed, progress=100, result=result)
    except Exception as e:
        jobs.update(job_id, status=JobStatus.failed, error=str(e))


@router.post("/analyze", response_model=JobResponse)
def analyze(body: AnalyzeRequest, background_tasks: BackgroundTasks):
    job_id = jobs.create()
    background_tasks.add_task(_run_analysis, job_id, body.repo)
    return JobResponse(job_id=job_id, status=JobStatus.pending)
