import random
import json
import torch
import os
import wikipedia
import datetime
from django.shortcuts import render
from django.http import JsonResponse

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

# Set the device to CUDA (GPU) if available or CPU if not
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Set the model path (from BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'chat', 'data.pth')

# Load intents from 'intents.json'
with open(os.path.join(BASE_DIR, 'chat', 'intents.json'), 'r') as json_data:
    intents = json.load(json_data)

# Load the trained model
data = torch.load(model_path)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initialize model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Fuze"

def clean_query(query):
    """Clean user query for better Wikipedia results"""
    trigger_phrases = [
        "who is", "what is", "tell me about", "define", "explain", "can you tell me about",
        "give me info about", "give me information about", "i want to learn about", "search wikipedia for"
    ]
    query = query.lower()
    for phrase in trigger_phrases:
        query = query.replace(phrase, "")
    return query.strip().title()

def search_wikipedia(query):
    """Fetch summary from Wikipedia"""
    try:
        summary = wikipedia.summary(clean_query(query), sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That’s a bit vague. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything about that on Wikipedia."
    except Exception:
        return "Oops! Something went wrong while searching Wikipedia."

def get_response(msg):
    """Get the chatbot's response based on user input."""
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        if tag == "wikipedia":
            return search_wikipedia(msg)
        
        # Dynamic Date
        if tag == "general" and any(kw in msg.lower() for kw in ["date", "day", "today"]):
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            return f"Today is {today}."

        for intent in intents['intents']:
            if tag == intent["intent"]:
                return random.choice(intent['responses'])

    # 🔁 Fallback to Wikipedia if it's a knowledge query
    if any(phrase in msg.lower() for phrase in ["what is", "who is", "tell me about", "explain", "define", "search wikipedia"]):
        return search_wikipedia(msg)

    return "I'm not sure I understand. Could you rephrase that?"


def chat_view(request):
    """Handle the chat interaction via AJAX POST"""
    if request.method == "POST":
        user_message = request.POST.get('user_message')
        bot_response = get_response(user_message)
        return JsonResponse({'response': bot_response})
    
    return render(request, 'chat.html')

def home(request):
    return render(request, 'home.html')

def handle_exit_command(sentence):
    exit_commands = ['quit', 'exit', 'bye']
    return sentence.lower() in exit_commands
