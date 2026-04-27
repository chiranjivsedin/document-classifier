from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


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
