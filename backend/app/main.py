from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.shortcuts import router as shortcuts_router

app = FastAPI(title="AI Shortcuts Generator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(shortcuts_router, prefix="/api/shortcuts", tags=["shortcuts"])
