import torch
from nltk_utils import bag_of_words, tokenize
from model import NeuralNet
import json
import os

# Load intents
with open("intents.json", "r") as f:
    intents = json.load(f)

# Load model
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

# Evaluation
correct = 0
total = 0

for intent in intents['intents']:
    tag = intent['intent']
    for example in intent['examples']:
        tokens = tokenize(example)
        bow = bag_of_words(tokens, all_words)
        bow = bow.reshape(1, bow.shape[0])
        bow = torch.from_numpy(bow)

        output = model(bow)
        _, predicted = torch.max(output, dim=1)
        predicted_tag = tags[predicted.item()]

        if predicted_tag == tag:
            correct += 1
        total += 1

accuracy = 100.0 * correct / total
print(f"Accuracy on training examples: {accuracy:.2f}%")
