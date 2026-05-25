from datasets import load_dataset
from transformers import AutoTokenizer

# Load dataset
dataset = load_dataset("ag_news")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased"
)

# Function applied to each row
def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True
    )

# Tokenize all rows
tokenized_dataset = dataset.map(
    tokenize_function
)

print("\nOriginal row:")
print(dataset["train"][0])

print("\nTokenized row:")
print(tokenized_dataset["train"][0])

tokenized_dataset = tokenized_dataset.remove_columns(["text"])

tokenized_dataset = tokenized_dataset.rename_column(
    "label",
    "labels"
)

tokenized_dataset.set_format("torch")

print("\nPrepared row:")
print(tokenized_dataset["train"][0])