from transformers import pipeline

# Load fine-tuned model
classifier = pipeline(
    "text-classification",
    model="./results/final_model"
)

# Verify labels
print("Model labels:")
print(classifier.model.config.id2label)

while True:

    text = input("\nEnter text (type 'exit' to stop): ")

    if text.lower() == "exit":
        break

    pred = classifier(text)[0]

    print("\nPredicted category:")
    print(pred["label"])

    print("\nConfidence:")
    print(f"{round(pred['score']*100,2)} %")