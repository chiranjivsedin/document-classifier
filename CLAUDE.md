# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Product context

Requirements and domain notes live in [`docs/requirements.md`](./docs/requirements.md). Read it before reasoning about feature scope, behavior, or trade-offs. Update it in the same PR as any feature work that changes scope — don't let docs drift from code.

## Status

Backend scaffolding is in place; source files are still empty stubs. `frontend/` is empty (React confirmed; meta-framework TBD). Re-run `/init` after real code lands so this file can document concrete behavior.

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

### Pipeline architecture (intent)

`services/pipeline.py` orchestrates the document-AI flow:

```
input doc → ocr.py → detector.py → extractor.py → classifier.py → result
```

- **`ocr.py`** — text extraction from raster/PDF input.
- **`detector.py`** — originally scaffolded for layout/region detection. The current spec only needs "image-PDF vs text-PDF" routing, so this module's role is open (rename / fold into `pipeline.py` / keep). See `docs/requirements.md`.
- **`extractor.py`** — pulls structured fields from detected regions + OCR output.
- **`classifier.py`** — final document-type label. **v1 uses hosted Gemini; v2 swaps to a fine-tuned Gemma SLM.** Keep the public interface stable so the swap is a drop-in, not a rewrite.
- **`pipeline.py`** — composes the above; the route in `api/routes.py` should call `pipeline`, not the individual stages directly.

This is the intended shape based on filenames; treat as a guide until the modules have content.

### Naming convention worth preserving

`schemas/` (Pydantic) is deliberately separate from any future `ml/` directory (model wrappers / weights). Don't conflate the two under a single `models/` — that ambiguity is the reason the original layout was refactored.

## Frontend (`frontend/`)

React. Specific meta-framework (Next.js / Vite / Remix / CRA) still TBD — see `docs/requirements.md`.

## Docs (`docs/`)

- [`requirements.md`](./docs/requirements.md) — product/domain requirements (preliminary, evolving).
