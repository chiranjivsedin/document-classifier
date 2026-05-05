import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

import pymupdf

from app.schemas.classification import ClassifyResponse
from app.services.classifier import Classifier
from app.services.ocr import OCREngine

logger = logging.getLogger(__name__)

PdfRouter = Callable[[bytes, str], Literal["text", "image"]]


@dataclass
class Pipeline:
    router: PdfRouter
    ocr: OCREngine
    classifier: Classifier

    async def process(
        self, file_bytes: bytes, content_type: str
    ) -> ClassifyResponse:
        t0 = time.perf_counter()

        route = self.router(file_bytes, content_type)
        t_route = time.perf_counter()

        if route == "text":
            text = _extract_text_pdf(file_bytes)
            ocr_s = 0.0
        else:
            text = await self.ocr.extract(_render_pages(file_bytes, content_type))
            ocr_s = time.perf_counter() - t_route

        t_ocr = time.perf_counter()
        result = await self.classifier.classify(text, source_route=route)
        t_classify = time.perf_counter()

        route_s = t_route - t0
        classify_s = t_classify - t_ocr
        total_s = t_classify - t0

        logger.info(
            "pipeline | route=%s  router=%.3fs  ocr=%.3fs  classify=%.3fs  total=%.3fs",
            route, route_s, ocr_s, classify_s, total_s,
        )

        return ClassifyResponse(
            predicted_class=result.predicted_class,
            confidence=result.confidence,
            reason=result.reason,
            route=route,
            ocr_used=route == "image",
        )


def _extract_text_pdf(file_bytes: bytes) -> str:
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        return "\f".join(page.get_text() for page in doc)


def _render_pages(file_bytes: bytes, content_type: str) -> list[bytes]:
    if content_type.startswith("image/"):
        return [file_bytes]
    pages: list[bytes] = []
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            pages.append(pix.tobytes("png"))
    return pages
