from datasets import load_dataset
from collections import Counter

dataset = load_dataset("ag_news")

small_train = dataset["train"].shuffle(seed=42).select(range(1000))

labels = small_train["label"]

label_map = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Technology"
}

counts = Counter(labels)

print("\nTraining distribution:")

for label in sorted(counts):
    print(
        f"{label_map[label]} : {counts[label]}"
    )