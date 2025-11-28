from celery import shared_task
import requests
import os
import json
from django.conf import settings
from .models import Project

PROFILE_CONTEXT = """
You are a helpful AI assistant for Veselin's Portfolio website. 
Your goal is to answer questions about Veselin based ONLY on the information below.
If the answer is not in the text, politely say you don't know but suggest contacting him directly.
Keep answers concise, professional, and friendly.

ABOUT VESELIN:
- Name: Veselin Veselinov
- Role: Junior Python Developer
- Education: 
  1. Language Learning High school "Geo Milev" Dobrich (Primary Language - German, Secondary Language - English).
  2. SoftUni (Python Web Developer) - Django, Rest API, PostgreSQL.
- Skills: Python, Django, FastAPI, Docker, PostgreSQL, C++, Electronics.
- Certificates: Python Advanced, Django Advanced, PostgreSQL, DSD II Diplom (German).
- Background: Passionate about the intersection of software and physical world (Electronics).
- Tools: PyCharm, Visual Studio Code, Visual Studio, SSMS, PgAdmin, Docker, Git
- Personal Info:
    I'm a dedicated and fast-learning junior
developer currently finishing my
training at SoftUni and recent High
school graduate, specializing in Python,
C++, and SQL. Through personal
projects, I've gained practical
experience in building software and
solving real-world problems. I'm eager
to apply my skills, keep learning, and
grow as part of a professional
development team.
- Interests: Engineering, Sports, Hiking, Alpinism, Guitar, Music

"""


def query_huggingface(payload):
    """
    Sends a request to the Hugging Face Inference API.
    """
    # UPDATED URL: Changed 'api-inference' to 'router'
    api_url = f"https://router.huggingface.co/models/{os.environ.get('HUGGINGFACE_MODEL', 'mistralai/Mistral-7B-Instruct-v0.3')}"
    headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY')}"}
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@shared_task
def get_chatbot_response(user_message):
    """
    Generates a response using a real LLM via Hugging Face API.
    """
    # 1. Fetch Dynamic Data (Projects from DB)
    projects = Project.objects.all()
    project_text = "PROJECTS:\n"
    if projects.exists():
        for p in projects:
            project_text += f"- {p.title} ({p.get_category_display()}): {p.description}. Tech: {p.tech_stack}.\n"
    else:
        project_text += "No projects uploaded yet.\n"

    # 2. Construct the Prompt
    # Mistral format: <s>[INST] System Instruction + User Message [/INST]
    full_prompt = f"<s>[INST] {PROFILE_CONTEXT}\n\n{project_text}\n\nUSER QUESTION: {user_message} [/INST]"

    # 3. Call AI
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    if not api_key:
        return "I am currently offline (API Key missing). Please contact Veselin directly."

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 200,  # Limit response length
            "temperature": 0.7,  # Creativity
            "return_full_text": False
        }
    }

    response = query_huggingface(payload)

    # 4. Process Response
    try:
        # Hugging Face returns a list like [{'generated_text': '...'}]
        if isinstance(response, list) and len(response) > 0:
            return response[0].get('generated_text', 'I could not generate a response.').strip()
        elif 'error' in response:
            # Fallback if model is loading (common with free tier)
            if 'loading' in response['error'].lower():
                return "My brain is warming up (Model Loading). Please try again in 20 seconds!"
            return f"Error: {response['error']}"
        else:
            return "I'm having trouble thinking right now."

    except Exception as e:
        return f"Something went wrong: {str(e)}"