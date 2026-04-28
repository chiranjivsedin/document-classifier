import os

import pytest

from app.services.classifier import OllamaGemmaClassifier

CATEGORIES = ["invoice", "contract", "id_proof", "report", "other"]

pytestmark = pytest.mark.skipif(
    os.environ.get("LIVE_OLLAMA") != "1",
    reason="Set LIVE_OLLAMA=1 to run against a real Ollama daemon",
)


async def test_live_classifier_picks_a_known_category():
    clf = OllamaGemmaClassifier(
        host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        model=os.environ.get("OLLAMA_MODEL", "gemma3:4b"),
        categories=CATEGORIES,
    )
    result = await clf.classify(
        "INVOICE No. 12345\nBill To: Acme Corp\nTotal Due: $1,234.56\nTax: $123.45",
        source_route="text",
    )
    assert result.predicted_class in CATEGORIES
    assert 0.0 <= result.confidence <= 1.0
