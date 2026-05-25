from datasets import load_dataset

dataset = load_dataset("ag_news")

print(dataset)

print("\nFirst training example:")
print(dataset["train"][0])