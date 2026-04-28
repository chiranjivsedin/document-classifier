# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Product context

Requirements and domain notes live in [`docs/requirements.md`](./docs/requirements.md). Read it before reasoning about feature scope, behavior, or trade-offs. Update it in the same PR as any feature work that changes scope — don't let docs drift from code.

## Status

v1 backend is implemented and tested on `feat/local-gemma-classifier`. `POST /classify` is live, backed by Ollama + `gemma3:4b` with a discrete RapidOCR stage. `frontend/` is empty (React confirmed; meta-framework TBD).

## Backend (`backend/`)

Managed with **[uv](https://docs.astral.sh/uv/)**. Python pinned to **3.12** (`.python-version`) — chosen over 3.14 because most OCR / ML wheels (PyTorch, paddleocr, easyocr, opencv-python, pytesseract, transformers) don't ship 3.14 wheels yet. Dependencies live in `pyproject.toml`; there is no `requirements.txt`.

### Common commands

Run from `backend/`:

```bash
uv sync                                     # install runtime + dev deps into .venv
uv add <pkg>                                # add a runtime dependency
uv add --dev <pkg>                          # add a dev dependency
uv run uvicorn app.main:app --reload        # dev server (FastAPI hot reload)
uv run pytest                               # run all tests
uv run pytest tests/path/to/test_x.py::test_name   # single test
uv run ruff check .                         # lint
uv run ruff format .                        # format
```

### Layout

```
backend/
  pyproject.toml            # uv-managed deps + ruff + pytest config
  .python-version           # 3.12
  app/
    main.py                 # FastAPI app instance + lifespan
    api/routes.py           # HTTP routes (single module for now; split when >2 resources)
    core/config.py          # Settings, cross-cutting concerns
    schemas/                # Pydantic request/response models
    services/               # Pipeline stages (see below)
  tests/
    conftest.py
```

### Pipeline architecture

`services/pipeline.py` orchestrates the document-AI flow:

```
input doc → pdf_router.py → ocr.py (image route only) → classifier.py → result
```

- **`pdf_router.py`** — routes uploads to `"text"` or `"image"` path. Text PDFs: PyMuPDF extracts embedded text directly. Image PDFs / raster inputs: goes to OCR.
- **`ocr.py`** — `OCREngine` Protocol + `RapidOCREngine` (v1 default, `rapidocr-onnxruntime`). Swap engine by adding a sibling class and one branch in `core/deps.py`.
- **`classifier.py`** — `Classifier` Protocol + `OllamaGemmaClassifier` (v1, Ollama + `gemma3:4b`). v2 fine-tuned variant is a drop-in via the same Protocol.
- **`pipeline.py`** — composes the above; the route in `api/routes.py` calls `pipeline.process()`, not stages directly.
- **`core/deps.py`** — factory that builds the `Pipeline` from `Settings`; used as a FastAPI dependency (`get_pipeline`).

### API

- `POST /classify` — `multipart/form-data`, field `file` (PDF, PNG, JPEG). Returns `{predicted_class, confidence, reason, route, ocr_used}`.

### Naming convention worth preserving

`schemas/` (Pydantic) is deliberately separate from any future `ml/` directory (model wrappers / weights). Don't conflate the two under a single `models/` — that ambiguity is the reason the original layout was refactored.

## Frontend (`frontend/`)

React. Specific meta-framework (Next.js / Vite / Remix / CRA) still TBD — see `docs/requirements.md`.

## Docs (`docs/`)

- [`requirements.md`](./docs/requirements.md) — product/domain requirements (preliminary, evolving).
