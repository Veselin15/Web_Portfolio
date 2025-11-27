from celery import shared_task
import time
from .models import Project


# Махнахме Education и Certificate от импорта, защото не са модели

@shared_task
def get_chatbot_response(user_message):
    """
    Analyzes the user's message and returns a relevant response.
    """
    message = user_message.lower()


    # Логика за отговори
    if 'hello' in message or 'hi' in message or 'здравей' in message:
        return "Hello! I am Vlado's AI assistant. Ask me about his projects, skills, or education!"

    elif 'project' in message or 'проект' in message:
        # Тук ползваме базата данни, защото Project Е модел
        count = Project.objects.count()
        if count > 0:
            latest = Project.objects.first()  # ordering is -start_date
            return f"Vlado has worked on {count} amazing projects. His latest one is '{latest.title}'. You can verify it in the Projects section!"
        else:
            return "Vlado is currently uploading his projects. Stay tuned!"

    elif 'skill' in message or 'tech' in message or 'python' in message:
        return "Vlado is proficient in Python, Django, FastAPI, Docker, and PostgreSQL. He creates scalable web applications."

    elif 'contact' in message or 'email' in message or 'контакт' in message:
        return "You can contact Vlado via the form below on this page."

    elif 'education' in message or 'university' in message or 'degree' in message:
        # Тук връщаме статичен текст, вместо да питаме базата
        return "He holds a degree in Computer Science from the Technical University and has completed advanced courses at SoftUni."

    elif 'certificate' in message or 'cert' in message:
        return "Vlado has certificates in Python Advanced, Django Web Framework, and Docker & Kubernetes."

    else:
        return "I'm still learning! Try asking about 'projects', 'skills', or 'education'."