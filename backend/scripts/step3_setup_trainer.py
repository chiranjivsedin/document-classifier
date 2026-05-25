from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np
from sklearn.metrics import accuracy_score

MODEL_NAME = "distilbert-base-uncased"

# AG News label mappings — baked into the model so pipeline returns names directly
id2label = {0: "World", 1: "Sports", 2: "Business", 3: "Technology"}
label2id = {"World": 0, "Sports": 1, "Business": 2, "Technology": 3}

# Load dataset
dataset = load_dataset("ag_news")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Tokenize function
def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

# Tokenize dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.remove_columns(["text"])
tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
tokenized_dataset.set_format("torch")

# Training subset — 3000 examples gives enough signal per category
small_train = tokenized_dataset["train"].shuffle(seed=42).select(range(1000))
small_test  = tokenized_dataset["test"].shuffle(seed=42).select(range(200))

# Model — id2label/label2id baked in so saved model knows its own labels
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=4,
    id2label=id2label,
    label2id=label2id
)

# Accuracy metric — computed at end of each epoch
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, predictions)}

# Training settings
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=20,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train,
    eval_dataset=small_test,
    compute_metrics=compute_metrics
)

print("Starting training...")
trainer.train()

print("\nTraining completed")
print("Saving final model to ./results/final_model")
trainer.save_model("./results/final_model")
tokenizer.save_pretrained(
    "./results/final_model"
)