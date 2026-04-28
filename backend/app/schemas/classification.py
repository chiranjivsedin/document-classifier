from typing import Literal

from pydantic import BaseModel, Field


class ClassifyResponse(BaseModel):
    predicted_class: str
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    route: Literal["text", "image"]
    ocr_used: bool
