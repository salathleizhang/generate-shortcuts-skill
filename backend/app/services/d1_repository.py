"""Cloudflare D1 repository — access D1 via the Cloudflare REST API."""

from typing import Any, Optional
from uuid import uuid4

import httpx

from app.services.settings import (
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_D1_DATABASE_ID,
)

_D1_BASE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}/query"


def _d1_url() -> str:
    return _D1_BASE.format(
        account_id=CLOUDFLARE_ACCOUNT_ID,
        database_id=CLOUDFLARE_D1_DATABASE_ID,
    )


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }


def _execute(sql: str, params: Optional[list] = None) -> list[dict]:
    """Execute a single SQL statement against D1 and return result rows."""
    body: dict[str, Any] = {"sql": sql}
    if params:
        body["params"] = params

    resp = httpx.post(_d1_url(), json=body, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("success"):
        errors = data.get("errors", [])
        raise RuntimeError(f"D1 query failed: {errors}")

    results = data.get("result", [])
    if results and "results" in results[0]:
        return results[0]["results"]
    return []


def _new_id() -> str:
    return uuid4().hex


# ── Shortcuts ────────────────────────────────────────────────────────────

def create_shortcut(
    title: str,
    summary: str = "",
    author_id: Optional[str] = None,
    status: str = "draft",
) -> dict:
    shortcut_id = _new_id()
    slug = shortcut_id[:12]
    _execute(
        "INSERT INTO shortcuts (id, author_id, title, slug, summary, status) VALUES (?, ?, ?, ?, ?, ?)",
        [shortcut_id, author_id, title, slug, summary, status],
    )
    return {"id": shortcut_id, "slug": slug}


def get_shortcut(shortcut_id: str) -> Optional[dict]:
    rows = _execute("SELECT * FROM shortcuts WHERE id = ?", [shortcut_id])
    return rows[0] if rows else None


def update_shortcut(shortcut_id: str, **fields: Any) -> None:
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [shortcut_id]
    _execute(
        f"UPDATE shortcuts SET {set_clause}, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        values,
    )


# ── Shortcut Versions ───────────────────────────────────────────────────

def create_version(
    shortcut_id: str,
    unsigned_r2_key: str,
    plist_hash: str,
    version_number: int = 1,
    created_by: Optional[str] = None,
) -> dict:
    version_id = _new_id()
    _execute(
        "INSERT INTO shortcut_versions (id, shortcut_id, version_number, unsigned_r2_key, plist_hash, created_by) VALUES (?, ?, ?, ?, ?, ?)",
        [version_id, shortcut_id, version_number, unsigned_r2_key, plist_hash, created_by],
    )
    _execute(
        "UPDATE shortcuts SET current_version_id = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        [version_id, shortcut_id],
    )
    return {"id": version_id}


def get_version(version_id: str) -> Optional[dict]:
    rows = _execute("SELECT * FROM shortcut_versions WHERE id = ?", [version_id])
    return rows[0] if rows else None


def update_version(version_id: str, **fields: Any) -> None:
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [version_id]
    _execute(f"UPDATE shortcut_versions SET {set_clause} WHERE id = ?", values)


def get_versions_for_shortcut(shortcut_id: str) -> list[dict]:
    return _execute(
        "SELECT * FROM shortcut_versions WHERE shortcut_id = ? ORDER BY version_number DESC",
        [shortcut_id],
    )


# ── Signing Jobs ─────────────────────────────────────────────────────────

def create_signing_job(
    shortcut_id: str,
    version_id: str,
    input_r2_key: str,
) -> dict:
    job_id = _new_id()
    _execute(
        "INSERT INTO signing_jobs (id, shortcut_id, version_id, status, input_r2_key) VALUES (?, ?, ?, 'queued', ?)",
        [job_id, shortcut_id, version_id, input_r2_key],
    )
    return {"id": job_id}


def get_signing_job(job_id: str) -> Optional[dict]:
    rows = _execute("SELECT * FROM signing_jobs WHERE id = ?", [job_id])
    return rows[0] if rows else None


def claim_next_signing_job(worker_id: str) -> Optional[dict]:
    """Atomically claim the oldest queued signing job for this worker."""
    rows = _execute(
        "SELECT id FROM signing_jobs WHERE status IN ('queued', 'retrying') ORDER BY created_at ASC LIMIT 1",
    )
    if not rows:
        return None

    job_id = rows[0]["id"]
    _execute(
        "UPDATE signing_jobs SET status = 'running', locked_by = ?, locked_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), attempt_count = attempt_count + 1, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ? AND status IN ('queued', 'retrying')",
        [worker_id, job_id],
    )
    return get_signing_job(job_id)


def complete_signing_job(job_id: str, output_r2_key: str) -> None:
    _execute(
        "UPDATE signing_jobs SET status = 'succeeded', output_r2_key = ?, finished_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        [output_r2_key, job_id],
    )


def fail_signing_job(job_id: str, error: str, max_retries: int = 3) -> None:
    job = get_signing_job(job_id)
    if not job:
        return

    attempts = job.get("attempt_count", 0)
    new_status = "retrying" if attempts < max_retries else "failed"
    _execute(
        "UPDATE signing_jobs SET status = ?, last_error = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
        [new_status, error, job_id],
    )


# ── Community ────────────────────────────────────────────────────────────

def list_community_posts(category: Optional[str] = None, limit: int = 20, offset: int = 0) -> list[dict]:
    if category:
        return _execute(
            "SELECT cp.*, s.title, s.summary, s.download_count, s.like_count FROM community_posts cp JOIN shortcuts s ON cp.shortcut_id = s.id WHERE cp.category = ? AND cp.hidden_at IS NULL ORDER BY cp.rank_score DESC LIMIT ? OFFSET ?",
            [category, limit, offset],
        )
    return _execute(
        "SELECT cp.*, s.title, s.summary, s.download_count, s.like_count FROM community_posts cp JOIN shortcuts s ON cp.shortcut_id = s.id WHERE cp.hidden_at IS NULL ORDER BY cp.rank_score DESC LIMIT ? OFFSET ?",
        [limit, offset],
    )


def create_community_post(shortcut_id: str, category: str = "general") -> dict:
    post_id = _new_id()
    _execute(
        "INSERT INTO community_posts (id, shortcut_id, category) VALUES (?, ?, ?)",
        [post_id, shortcut_id, category],
    )
    return {"id": post_id}
