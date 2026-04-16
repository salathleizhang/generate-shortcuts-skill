"""Cloudflare R2 storage service (S3-compatible)."""

import hashlib
from pathlib import Path

import httpx

from app.services.settings import (
    R2_ACCESS_KEY_ID,
    R2_BUCKET,
    R2_ENDPOINT,
    R2_SECRET_ACCESS_KEY,
)


def _s3_client():
    """Create a lazy boto3 S3 client for R2."""
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError(
            "boto3 is not installed. Run `pip install boto3` in backend."
        ) from exc

    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def upload_file(local_path: Path, r2_key: str, content_type: str = "application/octet-stream") -> str:
    """Upload a local file to R2. Returns the R2 key."""
    client = _s3_client()
    client.upload_file(
        Filename=str(local_path),
        Bucket=R2_BUCKET,
        Key=r2_key,
        ExtraArgs={"ContentType": content_type},
    )
    return r2_key


def download_file(r2_key: str, local_path: Path) -> Path:
    """Download a file from R2 to a local path."""
    client = _s3_client()
    local_path.parent.mkdir(parents=True, exist_ok=True)
    client.download_file(
        Bucket=R2_BUCKET,
        Key=r2_key,
        Filename=str(local_path),
    )
    return local_path


def generate_presigned_url(r2_key: str, expires_in: int = 3600) -> str:
    """Generate a short-lived presigned download URL."""
    client = _s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": R2_BUCKET, "Key": r2_key},
        ExpiresIn=expires_in,
    )


def delete_file(r2_key: str) -> None:
    """Delete a file from R2."""
    client = _s3_client()
    client.delete_object(Bucket=R2_BUCKET, Key=r2_key)


def file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a local file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
