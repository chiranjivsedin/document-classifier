from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

import pymupdf

from app.schemas.classification import ClassifyResponse
from app.services.classifier import Classifier
from app.services.ocr import OCREngine

PdfRouter = Callable[[bytes, str], Literal["text", "image"]]


@dataclass
class Pipeline:
    router: PdfRouter
    ocr: OCREngine
    classifier: Classifier

    async def process(
        self, file_bytes: bytes, content_type: str
    ) -> ClassifyResponse:
        route = self.router(file_bytes, content_type)
        if route == "text":
            text = _extract_text_pdf(file_bytes)
        else:
            text = await self.ocr.extract(_render_pages(file_bytes, content_type))

        result = await self.classifier.classify(text, source_route=route)
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
