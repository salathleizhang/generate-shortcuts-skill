from fastapi import APIRouter, HTTPException

from app.services.d1_repository import get_signing_job
from app.services.settings import CLOUDFLARE_ACCOUNT_ID

router = APIRouter()


@router.get("/{job_id}")
def get_job(job_id: str):
    if not CLOUDFLARE_ACCOUNT_ID:
        raise HTTPException(status_code=501, detail="Cloud storage is not configured.")

    job = get_signing_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    return {
        "id": job["id"],
        "shortcut_id": job["shortcut_id"],
        "version_id": job["version_id"],
        "status": job["status"],
        "attempt_count": job["attempt_count"],
        "last_error": job.get("last_error"),
        "created_at": job["created_at"],
        "finished_at": job.get("finished_at"),
    }
