import pytest
from fastapi.testclient import TestClient

from app.core.deps import get_pipeline
from app.main import app
from app.schemas.classification import ClassifyResponse


class FakePipeline:
    def __init__(self):
        self.calls = []

    async def process(self, file_bytes: bytes, content_type: str) -> ClassifyResponse:
        self.calls.append((len(file_bytes), content_type))
        return ClassifyResponse(
            predicted_class="invoice",
            confidence=0.95,
            reason="fake",
            route="text",
            ocr_used=False,
        )


@pytest.fixture
def fake_pipeline():
    fake = FakePipeline()
    app.dependency_overrides[get_pipeline] = lambda: fake
    yield fake
    app.dependency_overrides.clear()


@pytest.fixture
def client(fake_pipeline):
    return TestClient(app)


def test_classify_returns_200_with_response_body(client, text_pdf_bytes: bytes):
    response = client.post(
        "/classify",
        files={"file": ("doc.pdf", text_pdf_bytes, "application/pdf")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_class"] == "invoice"
    assert body["route"] == "text"
    assert body["ocr_used"] is False


def test_classify_rejects_unsupported_content_type(client):
    response = client.post(
        "/classify",
        files={"file": ("doc.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_classify_rejects_empty_file(client):
    response = client.post(
        "/classify",
        files={"file": ("doc.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400
