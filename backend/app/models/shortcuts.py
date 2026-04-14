from typing import Literal, Optional

from pydantic import BaseModel, Field


class GenerateShortcutRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=4000)
    name: Optional[str] = Field(default=None, max_length=80)
    target: Literal["macOS", "iOS"] = "macOS"


class GenerateShortcutResponse(BaseModel):
    job_id: str
    status: Literal["ready"]
    name: str
    download_url: str
    requirements_url: str
    context_url: str
    signed: bool
    message: str
