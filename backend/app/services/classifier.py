import json
import re
from dataclasses import dataclass
from typing import Protocol

from ollama import AsyncClient

from app.core.prompt import DOCUMENT_CLASSIFIER_PROMPT


class ClassifierError(Exception):
    """Raised when the classifier cannot produce a result."""


class ClassifierParseError(ClassifierError):
    """Raised when the model output cannot be parsed into a result."""


@dataclass(frozen=True)
class ClassificationResult:
    predicted_class: str
    confidence: float
    reason: str


class Classifier(Protocol):
    async def classify(
        self, text: str, *, source_route: str
    ) -> ClassificationResult: ...


class OllamaGemmaClassifier:
    def __init__(self, host: str, model: str, categories: list[str]) -> None:
        self._client = AsyncClient(host=host)
        self._model = model
        self._categories = list(categories)

    async def classify(
        self, text: str, *, source_route: str
    ) -> ClassificationResult:
        prompt = DOCUMENT_CLASSIFIER_PROMPT.format(
            categories=", ".join(self._categories),
            categories_pipe=" | ".join(self._categories),
            source_route=source_route,
            text=text,
        )
        try:
            response = await self._client.generate(
                model=self._model,
                prompt=prompt,
                format="json",
            )
        except Exception as exc:  # noqa: BLE001
            raise ClassifierError(f"Ollama request failed: {exc}") from exc

        raw = getattr(response, "response", None)
        if raw is None and isinstance(response, dict):
            raw = response.get("response", "")
        return _parse_response(raw or "", self._categories)


def _parse_response(raw: str, categories: list[str]) -> ClassificationResult:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ClassifierParseError(f"No JSON object found in: {raw!r}")
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise ClassifierParseError(f"Invalid JSON: {match.group(0)!r}") from exc

    cls = data.get("class")
    if cls not in categories:
        cls = "other" if "other" in categories else categories[0]

    try:
        confidence = float(data.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    reason = str(data.get("reason", "")).strip()
    return ClassificationResult(
        predicted_class=cls, confidence=confidence, reason=reason
    )
