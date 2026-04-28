from app.services.ocr import RapidOCREngine


async def test_rapidocr_extracts_some_text(text_image_bytes: bytes):
    engine = RapidOCREngine()
    text = await engine.extract([text_image_bytes])
    # OCR is fuzzy; assert non-empty rather than exact match.
    assert text.strip() != ""
