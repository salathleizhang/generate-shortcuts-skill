from typing import Optional

from app.models.shortcuts import GenerateShortcutRequest, GenerateShortcutResponse
from app.services.d1_repository import create_shortcut, create_version, create_signing_job
from app.services.file_store import create_job_dir, write_job_metadata
from app.services.gemini_client import generate_requirements_document, generate_shortcut_plist
from app.services.name_resolver import apply_shortcut_name, resolve_shortcut_name
from app.services.plist_builder import write_shortcut_plist
from app.services.prompt_builder import build_requirements_prompt, build_shortcut_prompt
from app.services.r2_storage import upload_file, file_hash
from app.services.settings import CLOUDFLARE_ACCOUNT_ID
from app.services.signer import sign_shortcut
from app.services.validator import validate_shortcut_file


def generate_shortcut_cloud(request: GenerateShortcutRequest, author_id: Optional[str] = None) -> GenerateShortcutResponse:
    """Generate a shortcut with D1 + R2 cloud storage."""
    job_id, job_dir = create_job_dir()
    requirements_path = job_dir / "requirements.md"
    context_path = job_dir / "context_manifest.md"
    unsigned_path = job_dir / "unsigned.shortcut"

    # Generate requirements and shortcut plist via LLM
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

    # Upload unsigned file to R2
    plist_file_hash = file_hash(unsigned_path)
    unsigned_r2_key = f"unsigned/{job_id}/unsigned.shortcut"
    upload_file(unsigned_path, unsigned_r2_key)

    # Create records in D1
    sc = create_shortcut(title=shortcut_name, summary=request.prompt[:200], status="pending_signing", author_id=author_id)
    ver = create_version(
        shortcut_id=sc["id"],
        unsigned_r2_key=unsigned_r2_key,
        plist_hash=plist_file_hash,
    )
    signing_job = create_signing_job(
        shortcut_id=sc["id"],
        version_id=ver["id"],
        input_r2_key=unsigned_r2_key,
    )

    return GenerateShortcutResponse(
        job_id=signing_job["id"],
        status="ready",
        name=shortcut_name,
        download_url=f"/api/shortcuts/download/{job_id}",
        requirements_url=f"/api/shortcuts/requirements/{job_id}",
        context_url=f"/api/shortcuts/context/{job_id}",
        signed=False,
        message="Shortcut generated. Signing job queued — the signing worker will process it shortly.",
    )


def generate_shortcut_local(request: GenerateShortcutRequest, author_id: Optional[str] = None) -> GenerateShortcutResponse:
    """Generate a shortcut with local-only storage (original flow)."""
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


def generate_shortcut(request: GenerateShortcutRequest, author_id: Optional[str] = None) -> GenerateShortcutResponse:
    """Route to cloud or local generation based on config."""
    if CLOUDFLARE_ACCOUNT_ID:
        return generate_shortcut_cloud(request, author_id=author_id)
    return generate_shortcut_local(request, author_id=author_id)
