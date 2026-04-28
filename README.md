# Document Classifier

AI-powered document classification pipeline — uploads a PDF or image, routes it through OCR if needed, and classifies it using a local Gemma model via Ollama.

**Stack:** FastAPI · uv · Python 3.12 · Ollama (`gemma3:4b`) · RapidOCR · PyMuPDF

## Prerequisites

- [Ollama](https://ollama.com) installed and running
- `gemma3:4b` pulled: `ollama pull gemma3:4b`
- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Dev quickstart

```bash
cd backend
uv sync                                   # install deps into .venv
uv run uvicorn app.main:app --reload      # dev server on http://localhost:8000
uv run pytest                             # run tests (unit + mocked, no Ollama needed)
```

## Classify a document

```bash
curl -F "file=@/path/to/document.pdf" http://localhost:8000/classify
```

**Accepted:** `application/pdf`, `image/png`, `image/jpeg`

**Response:**
```json
{
  "predicted_class": "invoice",
  "confidence": 0.92,
  "reason": "Contains invoice number, line items, and total due.",
  "route": "text",
  "ocr_used": false
}
```

**Categories:** `invoice` · `contract` · `id_proof` · `report` · `other`

## Pipeline

```
upload → pdf_router → ┬─ text-PDF: PyMuPDF text extract ──┐
                      └─ image-PDF / raster: RapidOCR ────┴→ Ollama (gemma3:4b) → result
```

Both the OCR engine and the classifier implement Protocols — swapping either is a one-class change.

## Live integration test

Requires Ollama running with `gemma3:4b`:

```bash
LIVE_OLLAMA=1 uv run pytest tests/integration -v
```

## Configuration

Set via environment variables or a `backend/.env` file:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama daemon URL |
| `OLLAMA_MODEL` | `gemma3:4b` | Model to use |
| `OCR_ENGINE` | `rapidocr` | OCR backend (only `rapidocr` in v1) |
| `DOCUMENT_CATEGORIES` | `["invoice","contract","id_proof","report","other"]` | Classification labels |

## API docs

Interactive docs available at `http://localhost:8000/docs` when the server is running.

See [`CLAUDE.md`](./CLAUDE.md) for architecture details and [`docs/requirements.md`](./docs/requirements.md) for product context.
