from celery import shared_task
import requests
import os
from .models import Project

# Context for the AI
PROFILE_CONTEXT = """
You are a helpful AI assistant for Veselin's Portfolio website. 
Your goal is to answer questions about Veselin based ONLY on the information below.
Keep answers concise, professional, and friendly.

ABOUT VESELIN:
- Name: Veselin
- Role: Junior Python Developer
- Education: Technical University (BSc CS), SoftUni (Python Web Dev).
- Skills: Python, Django, FastAPI, Docker, PostgreSQL, Electronics.
- Certificates: Python Advanced, Django Advanced, PostgreSQL.
"""


def query_raw_http(payload, model_id, api_key):
    """
    Sends a raw HTTP request to the model API.
    """
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.post(api_url, headers=headers, json=payload, timeout=20)
    return response


@shared_task
def get_chatbot_response(user_message):
    """
    Generates response using raw HTTP requests (most compatible method).
    """
    # 1. Fetch Data
    projects = Project.objects.all()
    project_text = "PROJECTS: " + ", ".join(
        [f"{p.title} ({p.tech_stack})" for p in projects]) if projects.exists() else "No projects yet."

    # 2. Setup Client
    api_key = os.environ.get('HUGGINGFACE_API_KEY')
    if not api_key:
        return "I am currently offline (API Key missing)."

    # List of models (Microsoft Phi-3.5 is extremely reliable on free tier)
    models = [
        "microsoft/Phi-3.5-mini-instruct",
        "HuggingFaceH4/zephyr-7b-beta",
        "google/gemma-1.1-7b-it"
    ]

    # 3. Construct Prompt (Phi-3 format)
    # <|system|>...<|user|>...<|assistant|>
    prompt = f"<|system|>\n{PROFILE_CONTEXT}\n{project_text}<|end|>\n<|user|>\n{user_message}<|end|>\n<|assistant|>"

    last_error = ""

    for model_id in models:
        print(f"--- DEBUG AI: Trying {model_id} via RAW HTTP ---")

        try:
            # Payload for text generation
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 250,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }

            response = query_raw_http(payload, model_id, api_key)

            # Check status
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    answer = result[0].get('generated_text', '').strip()
                    print(f"--- DEBUG AI: Success with {model_id} ---")
                    return answer if answer else "I am thinking, but words failed me."

            # Handle Loading
            elif response.status_code == 503:
                return "My brain is warming up (Model Loading). Please ask me again in 20 seconds!"

            else:
                error_msg = response.text
                print(f"--- DEBUG AI: Failed {model_id} ({response.status_code}): {error_msg} ---")
                last_error = f"{response.status_code} - {error_msg[:100]}"

        except Exception as e:
            print(f"--- DEBUG AI: Exception with {model_id}: {e} ---")
            last_error = str(e)
            continue

    return f"Brain Error: All models failed. Last error: {last_error}"
    # PROFILE_CONTEXT = """
    # You are a helpful AI assistant for Veselin's Portfolio website.
    # Your goal is to answer questions about Veselin based ONLY on the information below.
    # If the answer is not in the text, politely say you don't know but suggest contacting him directly.
    # Keep answers concise, professional, and friendly.
    #
    # ABOUT VESELIN:
    # - Name: Veselin Veselinov
    # - Role: Junior Python Developer
    # - Education:
    #   1. Language Learning High school "Geo Milev" Dobrich (Primary Language - German, Secondary Language - English).
    #   2. SoftUni (Python Web Developer) - Django, Rest API, PostgreSQL.
    # - Skills: Python, Django, FastAPI, Docker, PostgreSQL, C++, Electronics.
    # - Certificates: Python Advanced, Django Advanced, PostgreSQL, DSD II Diplom (German).
    # - Background: Passionate about the intersection of software and physical world (Electronics).
    # - Tools: PyCharm, Visual Studio Code, Visual Studio, SSMS, PgAdmin, Docker, Git
    # - Personal Info:
    #     I'm a dedicated and fast-learning junior
    # developer currently finishing my
    # training at SoftUni and recent High
    # school graduate, specializing in Python,
    # C++, and SQL. Through personal
    # projects, I've gained practical
    # experience in building software and
    # solving real-world problems. I'm eager
    # to apply my skills, keep learning, and
    # grow as part of a professional
    # development team.
    # - Interests: Engineering, Sports, Hiking, Alpinism, Guitar, Music
    #
    # """