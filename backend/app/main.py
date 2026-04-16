from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.shortcuts import router as shortcuts_router
from app.api.jobs import router as jobs_router
from app.api.community import router as community_router
from app.api.users import router as users_router
from app.services.settings import APP_BASE_URL, APP_ENV

app = FastAPI(title="AI Shortcuts Generator", version="0.2.0")

# CORS: allow local dev and production frontend
allowed_origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]
if APP_BASE_URL and APP_BASE_URL not in allowed_origins:
    allowed_origins.append(APP_BASE_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": APP_ENV}


app.include_router(shortcuts_router, prefix="/api/shortcuts", tags=["shortcuts"])
app.include_router(jobs_router, prefix="/api/jobs", tags=["jobs"])
app.include_router(community_router, prefix="/api/community", tags=["community"])
app.include_router(users_router, prefix="/api", tags=["users"])
