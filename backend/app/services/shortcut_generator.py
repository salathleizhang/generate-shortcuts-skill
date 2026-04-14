from app.models.shortcuts import GenerateShortcutRequest, GenerateShortcutResponse
from app.services.file_store import create_job_dir, write_job_metadata
from app.services.gemini_client import generate_requirements_document, generate_shortcut_plist
from app.services.name_resolver import apply_shortcut_name, resolve_shortcut_name
from app.services.plist_builder import write_shortcut_plist
from app.services.prompt_builder import build_requirements_prompt, build_shortcut_prompt
from app.services.signer import sign_shortcut
from app.services.validator import validate_shortcut_file


def generate_shortcut(request: GenerateShortcutRequest) -> GenerateShortcutResponse:
    job_id, job_dir = create_job_dir()
    requirements_path = job_dir / "requirements.md"
    context_path = job_dir / "context_manifest.md"
    unsigned_path = job_dir / "unsigned.shortcut"
    signed_path = job_dir / "signed.shortcut"

    requirements_prompt = build_requirements_prompt(request)
    context_path.write_text(requirements_prompt.context_manifest, encoding="utf-8")
    requirements_doc = generate_requirements_document(requirements_prompt.prompt)
    requirements_path.write_text(requirements_doc + "\n", encoding="utf-8")
    shortcut_name = resolve_shortcut_name(request, requirements_doc)
    write_job_metadata(job_dir, shortcut_name)

    shortcut_prompt = build_shortcut_prompt(request, requirements_doc)
    shortcut = generate_shortcut_plist(shortcut_prompt.prompt)
    shortcut = apply_shortcut_name(shortcut, shortcut_name)
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
        name=shortcut_name,
        download_url=f"/api/shortcuts/download/{job_id}",
        requirements_url=f"/api/shortcuts/requirements/{job_id}",
        context_url=f"/api/shortcuts/context/{job_id}",
        signed=signed,
        message=message,
    )
