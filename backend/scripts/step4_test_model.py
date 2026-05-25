from datasets import load_dataset
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./results/final_model"
)

# Verify model knows its own labels
print("Model labels:")
print(classifier.model.config.id2label)

dataset = load_dataset("ag_news")

print(f"Dateset: {dataset}")
print("\n--- Predictions on AG News test set ---")

for i in range(10):
    text = dataset["test"][i]["text"]

    actual = classifier.model.config.id2label[
        dataset["test"][i]["label"]
    ]

    pred = classifier(text)[0]

    match = "✓" if pred["label"] == actual else "✗"

    print(f"\n{match} Text: {text[:80]}...")
    print(f"Actual: {actual}")
    print(
        f"Predicted: {pred['label']} "
        f"({round(pred['score']*100,1)}%)"
    )


# from datasets import load_dataset
# from transformers import pipeline

# classifier = pipeline(
#     "text-classification",
#     model="./results/final_model"
# )

# dataset = load_dataset("ag_news")

# print("Model labels:")
# print(classifier.model.config.id2label)

# # One example from each category
# examples = [
#     ("India wins cricket world cup final", "Sports"),
#     ("Stock market rises after strong investor confidence", "Business"),
#     ("UN discusses global climate policy", "World"),
#     ("Apple launches new AI processor", "Technology")
# ]

# print("\n--- Manual category testing ---")

# for text, actual in examples:

#     pred = classifier(text)[0]

#     match = "✓" if pred["label"] == actual else "✗"

#     print(f"\n{match} Text: {text}")
#     print(f"Actual: {actual}")
#     print(
#         f"Predicted: {pred['label']} "
#         f"({round(pred['score']*100,1)}%)"
#     )