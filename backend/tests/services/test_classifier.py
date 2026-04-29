import pytest
from pytest_httpx import HTTPXMock

from app.services.classifier import (
    ClassifierParseError,
    OllamaGemmaClassifier,
)


def _ollama_response(content: str) -> dict:
    return {
        "model": "gemma3:4b",
        "response": content,
        "done": True,
        "done_reason": "stop",
    }


CATEGORIES = ["invoice", "contract", "id_proof", "report", "other"]


async def test_classify_returns_parsed_result(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:11434/api/generate",
        json=_ollama_response(
            '{"class": "invoice", "confidence": 0.9, "reason": "has invoice no"}'
        ),
    )
    clf = OllamaGemmaClassifier(
        host="http://localhost:11434", model="gemma3:4b", categories=CATEGORIES
    )
    result = await clf.classify("INVOICE 12345", source_route="text")
    assert result.predicted_class == "invoice"
    assert result.confidence == 0.9
    assert "invoice" in result.reason.lower()


async def test_classify_tolerates_prose_around_json(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:11434/api/generate",
        json=_ollama_response(
            'Here is the answer: {"class": "report", "confidence": 0.7, "reason": "annual"}'
        ),
    )
    clf = OllamaGemmaClassifier(
        host="http://localhost:11434", model="gemma3:4b", categories=CATEGORIES
    )
    result = await clf.classify("Annual Report 2025", source_route="text")
    assert result.predicted_class == "report"


async def test_classify_falls_back_to_other_for_unknown_class(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:11434/api/generate",
        json=_ollama_response(
            '{"class": "made_up", "confidence": 0.3, "reason": "?"}'
        ),
    )
    clf = OllamaGemmaClassifier(
        host="http://localhost:11434", model="gemma3:4b", categories=CATEGORIES
    )
    result = await clf.classify("???", source_route="text")
    assert result.predicted_class == "other"


async def test_classify_clips_confidence_into_unit_interval(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:11434/api/generate",
        json=_ollama_response(
            '{"class": "invoice", "confidence": 1.7, "reason": "x"}'
        ),
    )
    clf = OllamaGemmaClassifier(
        host="http://localhost:11434", model="gemma3:4b", categories=CATEGORIES
    )
    result = await clf.classify("???", source_route="text")
    assert result.confidence == 1.0


async def test_classify_raises_on_unparseable_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:11434/api/generate",
        json=_ollama_response("absolutely no json here"),
    )
    clf = OllamaGemmaClassifier(
        host="http://localhost:11434", model="gemma3:4b", categories=CATEGORIES
    )
    with pytest.raises(ClassifierParseError):
        await clf.classify("???", source_route="text")
