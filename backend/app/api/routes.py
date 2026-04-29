from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.deps import get_pipeline
from app.schemas.classification import ClassifyResponse
from app.services.classifier import ClassifierError
from app.services.pipeline import Pipeline

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}


@router.get("/")
def root() -> dict[str, str]:
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.post("/classify", response_model=ClassifyResponse)
async def classify(
    file: UploadFile = File(...),
    pipeline: Pipeline = Depends(get_pipeline),
) -> ClassifyResponse:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type: {file.content_type}",
        )
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")
    try:
        return await pipeline.process(file_bytes, file.content_type)
    except ClassifierError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
