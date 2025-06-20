# 🤖 Fuze Chatbot

Fuze is a modern AI-powered chatbot built using **PyTorch**, **Django**, and a custom-trained intent classification model. It also integrates external APIs like **Wikipedia** to respond intelligently to user queries.



---

## 🌟 Features

- 💬 Intent-based NLP chatbot with PyTorch
- 📚 Wikipedia integration (via `wikipedia` Python package)
- 🔥 Django backend + AJAX-based chat
- 🎓 Trained on custom `intents.json`
- 🎯 100% accuracy on training dataset

---

## 🧠 Tech Stack

| Layer        | Tech                           |
|--------------|--------------------------------|
| Backend      | Django, PyTorch                |
| Frontend     | HTML, CSS, jQuery (AJAX)       |
| NLP Tools    | NLTK, NumPy, Wikipedia API     |


---

## 📁 Project Structure
chatbot/
├── chat/ # Django app
│ ├── templates/ # chat.html frontend
│ ├── static/ # CSS and assets
│ ├── model.py # PyTorch NeuralNet class
│ ├── nltk_utils.py # Tokenization & bag-of-words
│ ├── train.py # Model training script
│ ├── views.py # Core chatbot logic
│ ├── intents.json # Dataset for training
│ └── data.pth # Trained model
├── chatbot/ # Django project settings
├── manage.py
└── README.md


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chatbot.git
cd chatbot

```

### 2.Create and activate virtual environment
python -m venv env
source env/bin/activate      # macOS/Linux
env\Scripts\activate.bat     # Windows

### 3.Install dependencies
```bash
pip install -r requirements.txt
```

### 4.Train 
```bash
cd chat
python train.py
```
#This will generate data.pth — the trained model saved to disk.

### 5.Run the server
```bash
cd chatbot
python manage.py runserver
```


