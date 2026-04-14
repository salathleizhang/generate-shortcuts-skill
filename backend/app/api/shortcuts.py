from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.shortcuts import GenerateShortcutRequest, GenerateShortcutResponse
from app.services.file_store import get_context_file, get_download_file, get_requirements_file
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
    download_file = get_download_file(job_id)
    if download_file is None:
        raise HTTPException(status_code=404, detail="Shortcut file not found.")

    return FileResponse(
        path=download_file.path,
        media_type="application/octet-stream",
        filename=download_file.filename,
    )


@router.get("/requirements/{job_id}")
def requirements(job_id: str) -> FileResponse:
    file_path = get_requirements_file(job_id)
    if file_path is None:
        raise HTTPException(status_code=404, detail="Requirements document not found.")

    return FileResponse(
        path=file_path,
        media_type="text/markdown; charset=utf-8",
        filename=file_path.name,
    )


@router.get("/context/{job_id}")
def context(job_id: str) -> FileResponse:
    file_path = get_context_file(job_id)
    if file_path is None:
        raise HTTPException(status_code=404, detail="Context manifest not found.")

    return FileResponse(
        path=file_path,
        media_type="text/markdown; charset=utf-8",
        filename=file_path.name,
    )
