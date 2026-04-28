import asyncio
import io
from typing import Protocol

import numpy as np
from PIL import Image


class OCREngine(Protocol):
    async def extract(self, page_images: list[bytes]) -> str: ...


class RapidOCREngine:
    """OCR engine backed by rapidocr-onnxruntime."""

    def __init__(self) -> None:
        from rapidocr_onnxruntime import RapidOCR

        self._engine = RapidOCR()

    async def extract(self, page_images: list[bytes]) -> str:
        return await asyncio.to_thread(self._extract_sync, page_images)

    def _extract_sync(self, page_images: list[bytes]) -> str:
        pages: list[str] = []
        for image_bytes in page_images:
            img = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
            result, _ = self._engine(img)
            text = "\n".join(line[1] for line in (result or []))
            pages.append(text)
        return "\f".join(pages)
