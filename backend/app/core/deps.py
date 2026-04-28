from functools import lru_cache

from app.core.config import Settings, settings
from app.services.classifier import OllamaGemmaClassifier
from app.services.ocr import OCREngine, RapidOCREngine
from app.services.pdf_router import route as pdf_route
from app.services.pipeline import Pipeline


def _build_ocr(engine_name: str) -> OCREngine:
    if engine_name == "rapidocr":
        return RapidOCREngine()
    raise ValueError(f"Unsupported OCR_ENGINE: {engine_name!r}")


def build_pipeline(s: Settings) -> Pipeline:
    return Pipeline(
        router=pdf_route,
        ocr=_build_ocr(s.OCR_ENGINE),
        classifier=OllamaGemmaClassifier(
            host=s.OLLAMA_HOST,
            model=s.OLLAMA_MODEL,
            categories=s.DOCUMENT_CATEGORIES,
        ),
    )


@lru_cache
def get_pipeline() -> Pipeline:
    """FastAPI dependency. Cached per-process so RapidOCR ONNX session loads once."""
    return build_pipeline(settings)
