"""Signing worker — polls D1 for queued signing jobs, signs on macOS, uploads to R2.

Run as a standalone process:
    python -m app.workers.signing_worker
"""

import logging
import platform
import time
from pathlib import Path
from uuid import uuid4

from app.services.d1_repository import (
    claim_next_signing_job,
    complete_signing_job,
    fail_signing_job,
    update_version,
    update_shortcut,
)
from app.services.r2_storage import download_file, upload_file, file_hash
from app.services.settings import JOBS_ROOT
from app.services.signer import sign_shortcut

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("signing-worker")

WORKER_ID = f"mac-{platform.node()}-{uuid4().hex[:6]}"
POLL_INTERVAL = 5  # seconds


def process_job(job: dict) -> None:
    """Download unsigned file, sign it, upload signed file, update D1."""
    job_id = job["id"]
    version_id = job["version_id"]
    shortcut_id = job["shortcut_id"]
    input_r2_key = job["input_r2_key"]

    work_dir = JOBS_ROOT / f"signing_{job_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    unsigned_path = work_dir / "unsigned.shortcut"
    signed_path = work_dir / "signed.shortcut"

    try:
        # Download unsigned file from R2
        logger.info("Job %s: downloading %s", job_id, input_r2_key)
        download_file(input_r2_key, unsigned_path)

        # Sign with macOS shortcuts CLI
        logger.info("Job %s: signing shortcut", job_id)
        signed = sign_shortcut(unsigned_path, signed_path)

        if not signed:
            raise RuntimeError("macOS shortcuts sign command failed or was unavailable")

        # Upload signed file to R2
        output_r2_key = f"signed/{shortcut_id}/{version_id}.shortcut"
        logger.info("Job %s: uploading signed file to %s", job_id, output_r2_key)
        upload_file(signed_path, output_r2_key)

        signed_file_hash = file_hash(signed_path)

        # Update D1 records
        complete_signing_job(job_id, output_r2_key)
        update_version(version_id, signed_r2_key=output_r2_key, signed_hash=signed_file_hash, signing_status="signed")
        update_shortcut(shortcut_id, status="signed")

        logger.info("Job %s: completed successfully", job_id)

    except Exception as exc:
        logger.error("Job %s: failed — %s", job_id, exc)
        fail_signing_job(job_id, str(exc))

    finally:
        # Clean up local temp files
        for f in work_dir.iterdir():
            f.unlink(missing_ok=True)
        work_dir.rmdir()


def run_worker() -> None:
    """Main worker loop — poll for jobs and process them."""
    logger.info("Signing worker started (id=%s)", WORKER_ID)

    while True:
        try:
            job = claim_next_signing_job(WORKER_ID)
            if job:
                process_job(job)
            else:
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Worker shutting down")
            break
        except Exception as exc:
            logger.error("Worker error: %s", exc)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_worker()
