from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.shortcuts import GenerateShortcutRequest, GenerateShortcutResponse
from app.services.file_store import get_download_file
from app.services.shortcut_generator import generate_shortcut

router = APIRouter()


@router.post("/generate", response_model=GenerateShortcutResponse)
def generate(request: GenerateShortcutRequest) -> GenerateShortcutResponse:
    try:
        return generate_shortcut(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/download/{job_id}")
def download(job_id: str) -> FileResponse:
    file_path = get_download_file(job_id)
    if file_path is None:
        raise HTTPException(status_code=404, detail="Shortcut file not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_path.name,
    )
