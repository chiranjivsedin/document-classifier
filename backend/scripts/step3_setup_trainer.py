from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np
from sklearn.metrics import accuracy_score

# Load dataset
dataset = load_dataset("ag_news")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased"
)

# Tokenize function
def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

# Tokenize dataset
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True
)

# Remove text column
tokenized_dataset = tokenized_dataset.remove_columns(
    ["text"]
)

# Rename label → labels
tokenized_dataset = tokenized_dataset.rename_column(
    "label",
    "labels"
)

# Convert to torch tensors
tokenized_dataset.set_format("torch")

# Smaller subset for faster demo training
small_train = tokenized_dataset["train"].shuffle(seed=42).select(range(1000))
small_test = tokenized_dataset["test"].shuffle(seed=42).select(range(200))

MODEL_NAME = "distilbert-base-uncased"

# Model — num_labels matches number of AG News categories
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=4
)

# Accuracy metric — computed at end of each epoch
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, predictions)}

# Training settings
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",        
    save_strategy="epoch",     
    logging_steps=20,
    load_best_model_at_end=True
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