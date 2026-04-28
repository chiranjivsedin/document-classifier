# Document Classifier AI

AI-powered document classification application using **React** on the frontend. The classifier ships in two phases:

- **v1 — local Gemma via Ollama** (`gemma3:4b`, zero/few-shot, prompt-engineered) — no hosted-API dependency, no labeled dataset needed.
- **v2 — fine-tuned Gemma SLM** trained on labeled documents collected during v1; same self-hosted setup, better accuracy.

> **Status:** preliminary — evolves as understanding deepens.
> Update in the same PR as feature work that changes scope.

## Workflow

1. **Document upload** — users upload documents (PDFs / images) into the application.
2. **Document type detection** — the system detects whether the uploaded file is:
   - Image-based PDF / scanned document → requires OCR
   - Text-based PDF → text can be extracted directly
3. **OCR processing (conditional)** — if the document is image-based, an OCR step converts the visual content into machine-readable text.
4. **Text extraction & preprocessing** — extracted text is cleaned, normalized, and prepared for model input.
5. **Document classification** — the active classifier (local Gemma via Ollama in v1, fine-tuned Gemma in v2) assigns a document type from the predefined category set: `invoice`, `contract`, `id_proof`, `report`, `other`.
6. **Response output** — the application returns:
   - Predicted document class
   - Confidence score
   - Optional extracted metadata / explanation

## Final goal

A smart document ingestion and classification pipeline that automatically handles both text PDFs and scanned/image PDFs, performs OCR when needed, and classifies documents accurately — initially via local Gemma (Ollama), transitioning to a fine-tuned Gemma SLM as a labeled dataset accumulates.

## Model strategy / phasing

| Phase  | Classifier                                           | Why                                                                                                               |
|--------|------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **v1** | Local Gemma via Ollama (`gemma3:4b`, prompt-engineered) | No labeled dataset and no hosted-API dependency; fully local; collect labeled production data along the way. |
| **v2** | Fine-tuned Gemma SLM, self-hosted via Ollama            | Higher accuracy; triggered once enough labeled data exists. Same infrastructure, better weights.             |

The pipeline shape (`pdf_router → ocr → classifier → response`) is identical across phases — only the **classifier** implementation swaps. `services/classifier.py` exposes a `Classifier` Protocol so v2 is a drop-in replacement, not a rewrite.

## Open questions / decisions to make

- **Frontend specifics.** React confirmed — which meta-framework (Next.js / Vite / Remix / plain CRA)? Auth requirement?
- **Deployment target.** On-prem at the customer's infra, cloud (which?), or Sedin-hosted? Especially relevant for v2 (Gemma needs GPU at inference).
- **Dataset for v2.** What triggers the v2 cutover — document count, labeling quality bar, calendar deadline? Labeling tooling? PII / sensitivity handling for stored documents?

## Glossary

- **SLM** — Small Language Model. Open-source models in the ~100M–4B parameter range (BERT, DistilBERT, Phi-3-mini, **Gemma-2B**), suitable for fine-tuning on commodity GPUs.
- **OCR** — Optical Character Recognition. Converts pixels to text.
- **Gemini** — Google's hosted multimodal LLM family, accessed via the `google-genai` SDK.
- **Gemma** — Google's open-weight SLM family (1B / 2B / 7B). Self-hostable, fine-tunable.
