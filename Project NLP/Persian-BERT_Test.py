from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained model tokenizer
tokenizer = BertTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased")

# Load pre-trained model
model = BertForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased")

# Example sentence
text = "من این محصول را دوست داشتم!"

# Tokenize input text
inputs = tokenizer(text, return_tensors="pt")

# Make prediction
outputs = model(**inputs)

# Get prediction
prediction = torch.argmax(outputs.logits)

# Print predicted label
print("Predicted label:", prediction.item())
