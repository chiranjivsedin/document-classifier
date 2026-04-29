from app.services.classifier import ClassificationResult
from app.services.pipeline import Pipeline


class FakeOCR:
    def __init__(self):
        self.calls = 0

    async def extract(self, page_images):
        self.calls += 1
        return "OCRed text"


class FakeClassifier:
    def __init__(self, result: ClassificationResult):
        self.result = result
        self.last_text: str | None = None
        self.last_route: str | None = None

    async def classify(self, text, *, source_route):
        self.last_text = text
        self.last_route = source_route
        return self.result


async def test_pipeline_text_route_skips_ocr(text_pdf_bytes: bytes):
    ocr = FakeOCR()
    clf = FakeClassifier(
        ClassificationResult(predicted_class="invoice", confidence=0.9, reason="x")
    )
    pipeline = Pipeline(router=lambda b, ct: "text", ocr=ocr, classifier=clf)

    response = await pipeline.process(text_pdf_bytes, "application/pdf")

    assert response.route == "text"
    assert response.ocr_used is False
    assert response.predicted_class == "invoice"
    assert ocr.calls == 0
    assert clf.last_route == "text"
    assert "INVOICE" in (clf.last_text or "").upper()


async def test_pipeline_image_route_uses_ocr(image_pdf_bytes: bytes):
    ocr = FakeOCR()
    clf = FakeClassifier(
        ClassificationResult(predicted_class="other", confidence=0.5, reason="x")
    )
    pipeline = Pipeline(router=lambda b, ct: "image", ocr=ocr, classifier=clf)

    response = await pipeline.process(image_pdf_bytes, "application/pdf")

    assert response.route == "image"
    assert response.ocr_used is True
    assert ocr.calls == 1
    assert clf.last_text == "OCRed text"


async def test_pipeline_image_route_handles_png_input(text_image_bytes: bytes):
    ocr = FakeOCR()
    clf = FakeClassifier(
        ClassificationResult(predicted_class="invoice", confidence=0.8, reason="x")
    )
    pipeline = Pipeline(router=lambda b, ct: "image", ocr=ocr, classifier=clf)

    response = await pipeline.process(text_image_bytes, "image/png")

    assert response.ocr_used is True
    assert ocr.calls == 1
