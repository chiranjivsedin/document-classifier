"""
Day 2 — DistilBERT Hands-On Exploration
Run each section one at a time. Read the output and understand what it means.
"""

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# ── STEP 1: Load tokenizer and model ──────────────────────────────────────────
# First run: downloads distilbert-base-uncased (~265MB) to your machine.
# Subsequent runs: loads from local cache — fully offline.
print("=" * 60)
print("STEP 1: Loading tokenizer and model")
print("=" * 60)

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

print("✓ Tokenizer loaded")
print("✓ Model loaded")
print(f"  Model parameters: {sum(p.numel() for p in model.parameters()):,}")


# ── STEP 2: Tokenization ──────────────────────────────────────────────────────
# Tokenization converts raw text into numbers the model can read.
# input_ids     → each word/subword mapped to a number
# attention_mask → 1 = real token, 0 = padding (ignored by model)
print("\n" + "=" * 60)
print("STEP 2: Tokenization — text → numbers")
print("=" * 60)

text = "Please find attached the invoice for the month of April."
inputs = tokenizer(text, return_tensors="pt")

print(f"\nOriginal text:\n  {text}")
print(f"\ninput_ids (each word → a number):\n  {inputs['input_ids']}")
print(f"\nattention_mask (1=real token, 0=padding):\n  {inputs['attention_mask']}")

# Decode tokens back to words — see how BERT splits text
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
print(f"\nTokens (how BERT reads the sentence):\n  {tokens}")
print("\n→ Notice [CLS] at the start — this token represents the whole sentence.")
print("→ Notice [SEP] at the end — marks end of input.")
print("→ Some words are split into subwords (e.g. 'invoice' may stay whole or split).")


# ── STEP 3: Forward pass ──────────────────────────────────────────────────────
# Passing the tokenized input through the model.
# logits = raw scores for each category (not probabilities yet).
# The model has 2 labels by default (positive/negative) — we will change this
# when we fine-tune for our document categories.
print("\n" + "=" * 60)
print("STEP 3: Forward pass — model reads the tokens")
print("=" * 60)

with torch.no_grad():
    outputs = model(**inputs)

print(f"\nRaw logits (scores per category):\n  {outputs.logits}")
print(f"\nShape: {outputs.logits.shape} → [1 document, 2 categories]")
print("\n→ These scores are meaningless right now — the model has NOT been")
print("  fine-tuned on our data yet. After fine-tuning, these scores will")
print("  map directly to our document categories (invoice, contract, etc.)")


# ── STEP 4: Multiple sentences ────────────────────────────────────────────────
# In real use, we classify one document at a time.
# Here we tokenize two different document types to see how inputs differ.
print("\n" + "=" * 60)
print("STEP 4: Tokenizing different document types")
print("=" * 60)

samples = [
    "Please find attached the invoice for services rendered in April 2024.",
    "This agreement is entered into between Party A and Party B on this date.",
]

for i, sample in enumerate(samples):
    tokens = tokenizer.convert_ids_to_tokens(
        tokenizer(sample, return_tensors="pt")["input_ids"][0]
    )
    print(f"\nSample {i+1}: {sample[:60]}...")
    print(f"Tokens: {tokens}")


# ── STEP 5: What changes after fine-tuning ────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: What fine-tuning will change")
print("=" * 60)
print("""
Right now:
  - Model has 2 output labels (default — positive/negative sentiment)
  - Weights are pre-trained on general English text (Wikipedia, books)
  - Logits are meaningless for our task

After fine-tuning on BPCL labeled data:
  - Model will have N output labels (one per document category)
  - Weights will be updated to recognise invoice/contract/report patterns
  - Logits will map directly to our categories with meaningful confidence scores

That is all fine-tuning is — taking this pre-trained model and continuing
to train it on our specific labeled examples.
""")

print("✓ Day 2 exploration complete. Move to Day 3 — Trainer API.")
