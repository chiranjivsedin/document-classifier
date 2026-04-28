from typing import Literal

import pymupdf

TEXT_THRESHOLD_CHARS = 100


def route(file_bytes: bytes, content_type: str) -> Literal["text", "image"]:
    """
    Decide whether a document should go through direct text extraction
    or through the OCR path.

    Image content-types short-circuit to "image". For PDFs, sum the
    embedded text length across pages; below TEXT_THRESHOLD_CHARS routes
    as "image", otherwise "text".
    """
    if content_type.startswith("image/"):
        return "image"

    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        total = sum(len(page.get_text()) for page in doc)
    return "text" if total >= TEXT_THRESHOLD_CHARS else "image"
