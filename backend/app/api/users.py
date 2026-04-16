from fastapi import APIRouter, Depends

from app.services.auth import require_auth, sync_clerk_user

router = APIRouter()


@router.get("/me")
def get_me(clerk_user_id: str = Depends(require_auth)):
    user = sync_clerk_user(clerk_user_id)
    return user
