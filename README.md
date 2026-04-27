# Document Classifier

Document classification and extraction pipeline.

> **Status:** scaffolding only — pipeline stages are empty stubs.

**Stack:** FastAPI · uv · Python 3.12 · Google Gemini (`google-genai`)

See [`CLAUDE.md`](./CLAUDE.md) for the intended layout and pipeline shape.

## Dev quickstart

```bash
cd backend
uv sync                                   # install deps into .venv
uv run uvicorn app.main:app --reload      # dev server
uv run pytest                             # run tests
```
