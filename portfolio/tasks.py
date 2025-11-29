from celery import shared_task
import requests
import os
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

def query_gemini_raw(api_key, payload, model_name):
    """
    Sends raw HTTP request to Google Gemini API using the standard v1beta endpoint.
    """
    # 1. FIX: Changed URL structure to be explicitly correct for 1.5 models
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response


@shared_task
def get_chatbot_response(user_message):
    # 1. Fetch Data
    projects = Project.objects.all()
    project_text = "PROJECTS: " + ", ".join([p.title for p in projects]) if projects.exists() else "No projects yet."

    # 2. Setup
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return "I am currently offline (API Key missing)."

    # 3. MODELS TO TRY
    # We test 'gemini-1.5-flash' first. If that fails, 'gemini-2.0-flash-exp' is the newest.
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-2.0-flash-exp",  # Experimental but very fast if available
        "gemini-1.5-pro",
        "gemini-pro"
    ]

    # 4. Construct Prompt
    full_prompt = f"{PROFILE_CONTEXT}\n\nDATA: {project_text}\n\nUSER: {user_message}"

    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }

    last_error = ""

    for model in models_to_try:
        print(f"--- DEBUG GEMINI: Trying {model} ---")
        try:
            response = query_gemini_raw(api_key, payload, model)

            if response.status_code == 200:
                data = response.json()
                try:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    return answer.strip()
                except (KeyError, IndexError):
                    # If blocked by safety filters
                    return "I cannot answer that due to safety guidelines."

            else:
                error_msg = response.text
                print(f"--- DEBUG GEMINI: Failed {model} ({response.status_code}): {error_msg} ---")

                # Check for "User Location" error (400)
                if "User location is not supported" in error_msg:
                    return "AI is not available in your region (Google Geoblocking). Use VPN or a different API."

                last_error = f"{response.status_code} - {error_msg[:100]}"

        except Exception as e:
            print(f"--- DEBUG GEMINI: Exception {e} ---")
            last_error = str(e)
            continue

    return f"My brain is having trouble. (Error: {last_error})"
