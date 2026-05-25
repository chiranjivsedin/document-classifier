from transformers import pipeline

label_map = {
    "LABEL_0": "World",
    "LABEL_1": "Sports",
    "LABEL_2": "Business",
    "LABEL_3": "Technology"
}

classifier = pipeline(
    "text-classification",
    model="./results/final_model"
)

texts = [
    "Apple launches a new AI processor for smartphones",
    "India wins the cricket world cup series",
    "Stock market rises after investor confidence improves"
]

for text in texts:
    result = classifier(text)[0]

    predicted = label_map[result["label"]]

    print("\nText:")
    print(text)

    print("\nPredicted category:")
    print(predicted)

    print("Confidence:")
    print(round(result["score"] * 100,2), "%")