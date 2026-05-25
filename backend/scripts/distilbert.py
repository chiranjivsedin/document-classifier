# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# model_name = "distilbert-base-uncased"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(
#     model_name
# )

# text = "Purchase Order No: PO-123 Vendor: ABC Ltd"

# inputs = tokenizer(text, return_tensors="pt")

# print("\nInput IDs:")
# print(inputs["input_ids"])

# print("\nAttention Mask:")
# print(inputs["attention_mask"])

# tokens = tokenizer.convert_ids_to_tokens(
#     inputs["input_ids"][0]
# )

# print("\nTokens:")
# print(tokens)

# with torch.no_grad():
#     outputs = model(**inputs)

# print("\nLogits:")
# print(outputs.logits)

# print("\nLogits shape:")
# print(outputs.logits.shape)

# probabilities = torch.softmax(outputs.logits, dim=1)

# print("\nProbabilities:")
# print(probabilities)

# predicted_class = torch.argmax(probabilities, dim=1)

# print("\nPredicted class:")
# print(predicted_class.item())


from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load YOUR fine-tuned model
model_path = "./results/final_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForSequenceClassification.from_pretrained(
    model_path
)

text = "India wins cricket world cup final"

inputs = tokenizer(
    text,
    return_tensors="pt"
)

print("\nInput IDs:")
print(inputs["input_ids"])

print("\nAttention Mask:")
print(inputs["attention_mask"])

tokens = tokenizer.convert_ids_to_tokens(
    inputs["input_ids"][0]
)

print("\nTokens:")
print(tokens)

with torch.no_grad():
    outputs = model(**inputs)

print("\nLogits:")
print(outputs.logits)

probabilities = torch.softmax(
    outputs.logits,
    dim=1
)

print("\nProbabilities:")
print(probabilities)

predicted_class = torch.argmax(
    probabilities,
    dim=1
)

# Convert number → category name
predicted_label = model.config.id2label[
    predicted_class.item()
]

print("\nPredicted category:")
print(predicted_label)