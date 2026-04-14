import json
from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.services.settings import JOBS_ROOT


class DownloadFile:
    def __init__(self, path: Path, filename: str) -> None:
        self.path = path
        self.filename = filename


def create_job_dir() -> tuple[str, Path]:
    job_id = uuid4().hex
    job_dir = JOBS_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=False)
    return job_id, job_dir


def get_download_file(job_id: str) -> Optional[DownloadFile]:
    if not job_id.isalnum():
        return None

    job_dir = JOBS_ROOT / job_id
    signed_file = job_dir / "signed.shortcut"
    unsigned_file = job_dir / "unsigned.shortcut"
    filename = _get_download_filename(job_dir)

    if signed_file.exists():
        return DownloadFile(path=signed_file, filename=filename)

    if unsigned_file.exists():
        return DownloadFile(path=unsigned_file, filename=filename)

    return None


def write_job_metadata(job_dir: Path, shortcut_name: str) -> None:
    metadata = {
        "shortcut_name": shortcut_name,
        "download_filename": f"{_sanitize_filename(shortcut_name)}.shortcut",
    }
    (job_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def get_requirements_file(job_id: str) -> Optional[Path]:
    if not job_id.isalnum():
        return None

    requirements_file = JOBS_ROOT / job_id / "requirements.md"
    if requirements_file.exists():
        return requirements_file

    return None


def get_context_file(job_id: str) -> Optional[Path]:
    if not job_id.isalnum():
        return None

    context_file = JOBS_ROOT / job_id / "context_manifest.md"
    if context_file.exists():
        return context_file

    return None


def _get_download_filename(job_dir: Path) -> str:
    metadata_file = job_dir / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
            filename = metadata.get("download_filename")
            if isinstance(filename, str) and filename.endswith(".shortcut"):
                return filename
        except json.JSONDecodeError:
            pass

    return "shortcut.shortcut"


def _sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    cleaned = "".join("_" if char in invalid_chars else char for char in name)
    cleaned = " ".join(cleaned.split()).strip(". ")

    return cleaned[:80] or "shortcut"
