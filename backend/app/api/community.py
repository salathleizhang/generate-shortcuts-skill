from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.services.d1_repository import list_community_posts, get_shortcut
from app.services.settings import CLOUDFLARE_ACCOUNT_ID

router = APIRouter()


@router.get("")
def list_posts(
    category: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    if not CLOUDFLARE_ACCOUNT_ID:
        raise HTTPException(status_code=501, detail="Cloud storage is not configured.")

    posts = list_community_posts(category=category, limit=limit, offset=offset)
    return {"items": posts, "count": len(posts)}


@router.get("/{shortcut_id}")
def get_community_shortcut(shortcut_id: str):
    if not CLOUDFLARE_ACCOUNT_ID:
        raise HTTPException(status_code=501, detail="Cloud storage is not configured.")

    shortcut = get_shortcut(shortcut_id)
    if not shortcut or shortcut.get("status") not in ("published", "signed"):
        raise HTTPException(status_code=404, detail="Shortcut not found.")

    return shortcut
