DOCUMENT_CLASSIFIER_PROMPT = """\
You are a document-classification model. Classify the document below into ONE of these categories: {categories}.

Respond ONLY with a single JSON object of the form:
{{"class": "<{categories_pipe}>", "confidence": <float 0..1>, "reason": "<short reason>"}}

The text was extracted via the "{source_route}" route.

Document text:
---
{text}
---
"""
