from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import django

# --- CRITICAL: Setup Django setup inside FastAPI ---
# This allows FastAPI to use Django models and DB!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyPortfolio.settings')
django.setup()
# ---------------------------------------------------

app = FastAPI()

# Allow CORS so the browser can talk to port 8000 and 8001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/chat")
def read_root():
    return {"message": "Hello from FastAPI running inside Django project!"}

# Example of using a Celery task (we will create it later in Django)
# from web.tasks import my_task
# @app.post("/run-task")
# def run_task():
#     my_task.delay()
#     return {"status": "Task sent"}