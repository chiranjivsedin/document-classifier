# Document Classifier AI

AI-powered document classification application using **React** on the frontend. The classifier ships in two phases:

- **v1 — hosted Gemini** for fast iteration without a labeled dataset (zero/few-shot, prompt-engineered).
- **v2 — fine-tuned Gemma SLM** trained on labeled documents collected during v1; runs without external API dependency.

> **Status:** preliminary — evolves as understanding deepens.
> Update in the same PR as feature work that changes scope.

## Workflow

1. **Document upload** — users upload documents (PDFs / images) into the application.
2. **Document type detection** — the system detects whether the uploaded file is:
   - Image-based PDF / scanned document → requires OCR
   - Text-based PDF → text can be extracted directly
3. **OCR processing (conditional)** — if the document is image-based, an OCR step converts the visual content into machine-readable text.
4. **Text extraction & preprocessing** — extracted text is cleaned, normalized, and prepared for model input.
5. **Document classification** — the active classifier (Gemini in v1, fine-tuned Gemma in v2) assigns a document type from the predefined category set (e.g. invoice, contract, ID proof, report).
6. **Response output** — the application returns:
   - Predicted document class
   - Confidence score
   - Optional extracted metadata / explanation

## Final goal

A smart document ingestion and classification pipeline that automatically handles both text PDFs and scanned/image PDFs, performs OCR when needed, and classifies documents accurately — initially via hosted Gemini, transitioning to a fine-tuned Gemma SLM as a labeled dataset accumulates.

## Model strategy / phasing

| Phase  | Classifier                                           | Why                                                                                                               |
|--------|------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **v1** | Google Gemini (hosted, via `google-genai`)           | No labeled dataset needed; ship classification quickly; collect labeled production data along the way.            |
| **v2** | Fine-tuned Gemma SLM (e.g. Gemma-2B), self-hosted    | Lower per-request cost, no third-party data sharing, latency control. Triggered once enough labeled data exists.  |

The pipeline shape (`ocr → preprocess → classifier → response`) is identical across phases — only the **classifier** implementation swaps. `services/classifier.py` should expose a stable interface so v2 is a drop-in replacement, not a rewrite.

## Open questions / decisions to make

- **`detector.py` role.** The scaffold has a `services/detector.py` slot intended for layout/region detection. The workflow above only needs simpler "image-PDF vs text-PDF" routing. If layout detection isn't planned, `detector.py` should be removed (or renamed to `pdf_router.py`) and the routing logic folded into the pipeline.
- **Document categories.** Final list of classes? Examples in the spec are placeholders.
- **Frontend specifics.** React confirmed — which meta-framework (Next.js / Vite / Remix / plain CRA)? Auth requirement?
- **Deployment target.** On-prem at the customer's infra, cloud (which?), or Sedin-hosted? Especially relevant for v2 (Gemma needs GPU at inference).
- **Dataset for v2.** What triggers the v2 cutover — document count, labeling quality bar, calendar deadline? Labeling tooling? PII / sensitivity handling for stored documents?

## Glossary

- **SLM** — Small Language Model. Open-source models in the ~100M–4B parameter range (BERT, DistilBERT, Phi-3-mini, **Gemma-2B**), suitable for fine-tuning on commodity GPUs.
- **OCR** — Optical Character Recognition. Converts pixels to text.
- **Gemini** — Google's hosted multimodal LLM family, accessed via the `google-genai` SDK.
- **Gemma** — Google's open-weight SLM family (1B / 2B / 7B). Self-hostable, fine-tunable.
