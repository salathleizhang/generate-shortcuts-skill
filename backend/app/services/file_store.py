from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.services.settings import JOBS_ROOT


def create_job_dir() -> tuple[str, Path]:
    job_id = uuid4().hex
    job_dir = JOBS_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=False)
    return job_id, job_dir


def get_download_file(job_id: str) -> Optional[Path]:
    if not job_id.isalnum():
        return None

    job_dir = JOBS_ROOT / job_id
    signed_file = job_dir / "signed.shortcut"
    unsigned_file = job_dir / "unsigned.shortcut"

    if signed_file.exists():
        return signed_file

    if unsigned_file.exists():
        return unsigned_file

    return None
