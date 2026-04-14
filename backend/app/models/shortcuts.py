from typing import Literal

from pydantic import BaseModel, Field


class GenerateShortcutRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=4000)
    name: str = Field(..., min_length=1, max_length=80)
    target: Literal["macOS", "iOS"] = "macOS"


class GenerateShortcutResponse(BaseModel):
    job_id: str
    status: Literal["ready"]
    download_url: str
    signed: bool
    message: str
