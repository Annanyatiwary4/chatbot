from django.contrib import admin
from django.urls import path
from chat import views  # Import your chatbot views

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),  # Route for your chat page
]

