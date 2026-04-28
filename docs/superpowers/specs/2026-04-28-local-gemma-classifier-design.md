# Local Gemma Classifier (v1) — Design

**Date:** 2026-04-28
**Branch:** `feat/local-gemma-classifier`
**Status:** approved (brainstorming)

## Context

`docs/requirements.md` originally planned v1 = hosted Gemini, v2 = fine-tuned Gemma. We're skipping the hosted phase: v1 is now **Ollama + `gemma3:4b` running locally** (zero/few-shot, prompt-engineered). v2 (fine-tuning on labeled data) remains future work and reuses the same seams.

## Goals

- Working `POST /classify` endpoint by end of day, fully local, no hosted-API dependencies.
- Stage boundaries (`pdf_router`, `ocr`, `classifier`) are Protocol-based so v2 — and any OCR engine swap — is a drop-in replacement.

## Non-goals

- Frontend (`frontend/` stays empty).
- Field-level extraction (`services/extractor.py` deleted; reintroduce when post-classification extraction is actually needed).
- Layout / region detection.
- Auth, rate-limiting, multi-tenancy.
- Confidence calibration.

## Architecture

```
POST /classify (UploadFile)
        │
        ▼
  pipeline.process(file_bytes, content_type)
        │
        ▼
  pdf_router.route(file_bytes) ──► "text" | "image"
        │
        ├── "text"  → PyMuPDF.extract_text(file_bytes)
        └── "image" → ocr_engine.extract(rendered_pages)
        │
        ▼
  classifier.classify(text, route)
        │
        ▼
  ClassifyResponse (JSON)
```

## Module responsibilities

### `services/pdf_router.py` (replaces `detector.py`)

```python
def route(file_bytes: bytes, content_type: str) -> Literal["text", "image"]:
    """
    Image content-types short-circuit to "image".
    For PDFs: open with PyMuPDF, sum embedded text length across pages;
    return "image" if total < TEXT_THRESHOLD_CHARS, else "text".
    """
```

- `TEXT_THRESHOLD_CHARS = 100` (module constant).
- Pure function; no IO beyond PyMuPDF parsing.

### `services/ocr.py`

```python
class OCREngine(Protocol):
    async def extract(self, page_images: list[bytes]) -> str: ...

class RapidOCREngine:
    """Wraps rapidocr-onnxruntime. Joins per-page text with form-feed."""
    def __init__(self) -> None: ...
    async def extract(self, page_images: list[bytes]) -> str: ...
```

- v1 ships `RapidOCREngine` only.
- Adding `TesseractEngine` later = one new file + one branch in `core/deps.py`.
- PDF-page rendering (PyMuPDF → PNG bytes) lives in `pipeline.py`, not in `ocr.py` — keeps the OCR engine focused on `image-bytes → text`.

### `services/classifier.py`

```python
@dataclass(frozen=True)
class ClassificationResult:
    predicted_class: str
    confidence: float
    reason: str

class Classifier(Protocol):
    async def classify(self, text: str, *, source_route: str) -> ClassificationResult: ...

class OllamaGemmaClassifier:
    def __init__(self, host: str, model: str, categories: list[str]) -> None: ...
    async def classify(self, text: str, *, source_route: str) -> ClassificationResult: ...
```

- Uses the `ollama` Python client (`AsyncClient.generate` with `format="json"`).
- Prompt template lives next to the class as a module-level constant; lists categories and demands JSON output `{class, confidence, reason}`.
- Parser tolerates dirty output: extracts the first `{...}` block, validates against `ClassificationResult` fields, raises `ClassifierParseError` on failure.
- v2 fine-tuned classifier is a sibling class implementing the same `Classifier` Protocol.

### `services/pipeline.py`

```python
@dataclass
class Pipeline:
    router: PdfRouter            # Callable[[bytes, str], Literal["text", "image"]]
    ocr: OCREngine
    classifier: Classifier

    async def process(self, file_bytes: bytes, content_type: str) -> ClassifyResponse:
        route = self.router(file_bytes, content_type)
        text = (
            extract_text_pdf(file_bytes) if route == "text"
            else await self.ocr.extract(render_pages(file_bytes, content_type))
        )
        result = await self.classifier.classify(text, source_route=route)
        return ClassifyResponse(
            predicted_class=result.predicted_class,
            confidence=result.confidence,
            reason=result.reason,
            route=route,
            ocr_used=route == "image",
        )
```

- `extract_text_pdf` and `render_pages` are small private helpers in `pipeline.py` (PyMuPDF wrappers). They aren't worth their own module.

### `core/deps.py` (new)

Factory:

```python
def build_pipeline(settings: Settings) -> Pipeline: ...
def get_pipeline() -> Pipeline:  # FastAPI dependency, cached per-process
```

- `build_pipeline` selects OCR engine via `settings.OCR_ENGINE` (`"rapidocr"` only in v1 — anything else raises at startup).
- Classifier instantiated with `settings.OLLAMA_HOST`, `OLLAMA_MODEL`, `DOCUMENT_CATEGORIES`.

### `app/schemas/classification.py` (new)

```python
class ClassifyResponse(BaseModel):
    predicted_class: str
    confidence: float
    reason: str
    route: Literal["text", "image"]
    ocr_used: bool
```

## Config additions (`core/config.py`)

| Setting | Default | Notes |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | |
| `OLLAMA_MODEL` | `gemma3:4b` | |
| `OCR_ENGINE` | `rapidocr` | v1 accepts only this value |
| `DOCUMENT_CATEGORIES` | `["invoice", "contract", "id_proof", "report", "other"]` | |

Drop `GOOGLE_API_KEY`.

## API contract

`POST /classify` — `multipart/form-data`, single field `file` (`UploadFile`).

**Accepted content types:** `application/pdf`, `image/png`, `image/jpeg`. Anything else → `415 Unsupported Media Type`.

**Response 200:**

```json
{
  "predicted_class": "invoice",
  "confidence": 0.87,
  "reason": "Contains 'Invoice No.', 'Total Due', and a tax line.",
  "route": "text",
  "ocr_used": false
}
```

**Errors:**

- `400` — corrupt / unreadable file.
- `415` — unsupported content type.
- `502` — Ollama unreachable, non-2xx, or response un-parseable as JSON.

## Dependencies

```bash
uv add pymupdf rapidocr-onnxruntime ollama
uv remove google-genai
```

`google-genai` is dropped because there is no hosted-Gemini path in v1 anymore. Reintroduce only if a hosted fallback is later requested.

## Testing

| Test file | What it covers |
|---|---|
| `tests/services/test_pdf_router.py` | Fixtures: text PDF, scanned-image PDF, PNG. Asserts route. |
| `tests/services/test_ocr.py` | RapidOCR happy-path on a tiny rendered image fixture. |
| `tests/services/test_classifier.py` | `pytest-httpx` mocks Ollama HTTP. Verifies prompt structure, JSON parser tolerates extra prose around the JSON, raises on garbage. |
| `tests/services/test_pipeline.py` | Fakes for `ocr` + `classifier`; asserts orchestration glue + `ocr_used` flag. |
| `tests/api/test_classify.py` | FastAPI `TestClient` end-to-end with fakes injected via `app.dependency_overrides`. |
| `tests/integration/test_ollama_live.py` | Gated by `LIVE_OLLAMA=1`. One happy-path call against the running daemon. Skipped by default in CI. |

Add `pytest-httpx` to dev deps for mocking the `ollama` client's underlying httpx calls.

## Migration plan (future work, out of scope today)

- **v2 classifier (fine-tuned Gemma).** Implement `services/classifier_finetuned.py` against the same `Classifier` Protocol. Switch `core/deps.py` based on a new `CLASSIFIER_BACKEND` setting. No changes to `pipeline.py`, `routes.py`, or schemas.
- **OCR swap.** New engine class implementing `OCREngine`; one branch in `core/deps.py` keyed off `OCR_ENGINE`.
- **Multimodal collapse (optional).** `gemma3:4b` is multimodal; a future variant could feed page images directly to Gemma and bypass `ocr.py` for image-PDFs. Implement as a `MultimodalGemmaClassifier`; the `pipeline.process` branch on `route == "image"` would skip OCR when that backend is selected. Defer until OCR quality becomes the bottleneck.
- **Field extraction.** Reintroduce `services/extractor.py` when post-classification structured-field extraction is on the roadmap.

## Build sequence (today, on `feat/local-gemma-classifier`)

1. Commit this design doc.
2. Update deps: `uv add pymupdf rapidocr-onnxruntime ollama` · `uv add --dev pytest-httpx` · `uv remove google-genai`.
3. Update `core/config.py`: drop `GOOGLE_API_KEY`, add the four new settings.
4. Implement `services/pdf_router.py` + tests.
5. Implement `services/ocr.py` (`OCREngine` Protocol + `RapidOCREngine`) + tests.
6. Implement `services/classifier.py` (`Classifier` Protocol + `OllamaGemmaClassifier`) + tests using `respx`.
7. Implement `services/pipeline.py` (orchestration + private PyMuPDF helpers) + tests.
8. Implement `core/deps.py` factory.
9. Add `app/schemas/classification.py` and the `POST /classify` route in `app/api/routes.py` + endpoint test.
10. Delete `services/extractor.py` (empty stub).
11. Update `docs/requirements.md` and `CLAUDE.md` to reflect v1 = local Ollama+Gemma.
12. Manual smoke test against the running Ollama daemon with one text PDF and one scanned PDF.
13. Open PR.

## Open questions

None — all forks resolved during brainstorming.
