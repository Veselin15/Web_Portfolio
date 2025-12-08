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
- Role: Junior Software Developer / Junior Python Developer 
- Location: Dobrich, Bulgaria 
- Contact Information:
  - LinkedIn: linkedin.com/in/veselin-veselinov-a7bb9930a 
  - GitHub: github.com/Veselin15 

- Professional Summary:
  A dedicated and fast-learning junior developer currently finishing training at SoftUni and a recent High School graduate. Specializes in Python, C++, and SQL. Through personal projects, he has gained practical experience in building software and solving real-world problems. He is eager to apply skills, keep learning, and grow as part of a professional development team. Currently seeking an internship or junior position in Python backend development.

- Education:
  1. Software University (SoftUni) (02/2024 - Present):
     - Focus: Python Web Developer.
     - Key Modules Completed:
       - Python Advanced: Data structures, functional programming, recursion, file handling.
       - Python OOP: Object-oriented programming, design patterns, SOLID principles, unit testing.
       - Python ORM with Django: SQLAlchemy, model management, queries, relationships.
       - Databases with PostgreSQL: Relational design, SQL operations, transactions.
       - Django Basics: MTV architecture, views, forms, media handling.
       - Django Advanced: Authentication, User Models, Middlewares, Django REST (basic & advanced), Async operations, Unit Testing, Deployment.
  2. Language Learning High School "Geo Milev", Dobrich (09/2020 - 05/2025):
     - Primary Language: German.
     - Secondary Language: English.

- Technical Skills:
  - Languages: Python, C++, HTML, CSS, SQL, 35.
  - Frameworks & Libraries: Django, FastAPI, PyQt5, FaceNet, SVM.
  - Databases: PostgreSQL, Microsoft SQL Server.
  - Tools: PyCharm, Visual Studio Code, Visual Studio, SSMS, PgAdmin, Docker, Git.
  - Other: Electronics (passionate about the intersection of software and physical world).

- Soft Skills:
  - Attention to detail, Communication, Analysis, Teamwork & cooperation.

- Projects:
  1. Calories-Tracker]:
     - Description: A Django-based web app for tracking daily calorie intake and nutrition goals.
     - Features: User authentication, FatSecret API integration, responsive UI.
     - Link: https://caloriestracker-yy3h.onrender.com.
  2. Celebrity Face Recognition AI:
     - Description: Web app for celebrity face recognition using FaceNet for feature extraction and SVM for classification.
     - Features: Image uploads, guest access, result display.
  3. School Class Scheduling System:
     - Description: Python and PyQt5-based desktop application.
     - Features: Auto-generates conflict-free timetables based on session counts, teacher availability, and overlap detection.

- Certificates:
  - Python Advanced (09/2024) 
  - Python OOP (10/2024) 
  - PostgreSQL (01/2025) 
  - Python ORM (02/2025) 
  - Django Basics (05/2025) 
  - Django Advanced (06/2025) 
  - Deutsches Sprachdiplom II (German Language Diploma) 

- Languages:
  - Bulgarian (Native) 
  - English (Fluent) 
  - German (Advanced/DSD II) 

- Interests:
  - Engineering, Sports, Hiking, Alpinism, Guitar, Music, Puzzle Games, Movies, Video Games.
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
