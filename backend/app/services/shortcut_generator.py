from app.models.shortcuts import GenerateShortcutRequest, GenerateShortcutResponse
from app.services.file_store import create_job_dir
from app.services.plist_builder import build_demo_shortcut_plist, write_shortcut_plist
from app.services.signer import sign_shortcut
from app.services.validator import validate_shortcut_file


def generate_shortcut(request: GenerateShortcutRequest) -> GenerateShortcutResponse:
    job_id, job_dir = create_job_dir()
    unsigned_path = job_dir / "unsigned.shortcut"
    signed_path = job_dir / "signed.shortcut"

    shortcut = build_demo_shortcut_plist(name=request.name.strip(), prompt=request.prompt)
    write_shortcut_plist(shortcut, unsigned_path)
    validate_shortcut_file(unsigned_path)
    signed = sign_shortcut(unsigned_path, signed_path)

    message = (
        "Shortcut generated and signed successfully."
        if signed
        else "Shortcut generated. macOS signing was not available, so an unsigned fallback was returned."
    )

    return GenerateShortcutResponse(
        job_id=job_id,
        status="ready",
        download_url=f"/api/shortcuts/download/{job_id}",
        signed=signed,
        message=message,
    )
