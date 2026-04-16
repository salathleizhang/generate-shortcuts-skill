"""Clerk JWT verification and user sync."""

import logging
from typing import Optional

import httpx
import jwt
from fastapi import Depends, HTTPException, Request

from app.services.d1_repository import _execute, _new_id
from app.services.settings import CLERK_SECRET_KEY

logger = logging.getLogger("auth")

_jwks_cache: Optional[jwt.PyJWKClient] = None


def _get_jwks_client() -> jwt.PyJWKClient:
    global _jwks_cache
    if _jwks_cache is None:
        # Clerk JWKS endpoint — works for all Clerk instances
        # The issuer in the token tells us the exact URL, but we use the
        # well-known JWKS URI pattern for Clerk.
        _jwks_cache = jwt.PyJWKClient(
            uri="https://api.clerk.com/v1/jwks",
            headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
        )
    return _jwks_cache


def verify_clerk_token(token: str) -> dict:
    """Verify a Clerk session JWT and return the decoded payload."""
    try:
        client = _get_jwks_client()
        signing_key = client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as exc:
        logger.warning("Invalid Clerk token: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid token")


def get_clerk_user_id(request: Request) -> Optional[str]:
    """Extract Clerk user ID from Authorization header. Returns None if no token."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header[7:]
    payload = verify_clerk_token(token)
    return payload.get("sub")


def require_auth(request: Request) -> str:
    """FastAPI dependency — requires a valid Clerk session. Returns user ID."""
    user_id = get_clerk_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id


def optional_auth(request: Request) -> Optional[str]:
    """FastAPI dependency — returns user ID if authenticated, None otherwise."""
    return get_clerk_user_id(request)


def sync_clerk_user(clerk_user_id: str, email: str = "", display_name: str = "", avatar_url: str = "") -> dict:
    """Ensure the Clerk user exists in D1. Creates or updates as needed."""
    rows = _execute(
        "SELECT * FROM users WHERE auth_provider = 'clerk' AND provider_user_id = ?",
        [clerk_user_id],
    )
    if rows:
        user = rows[0]
        # Update if name/avatar changed
        if display_name and display_name != user.get("display_name"):
            _execute(
                "UPDATE users SET display_name = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                [display_name, user["id"]],
            )
        return user

    # Create new user
    user_id = _new_id()
    _execute(
        "INSERT INTO users (id, email, display_name, avatar_url, auth_provider, provider_user_id) VALUES (?, ?, ?, ?, 'clerk', ?)",
        [user_id, email, display_name, avatar_url, clerk_user_id],
    )
    return {"id": user_id, "email": email, "display_name": display_name, "auth_provider": "clerk", "provider_user_id": clerk_user_id}
