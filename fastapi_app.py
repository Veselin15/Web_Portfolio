from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
import os
import django

# 1. Setup Django environment inside FastAPI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web_Portfolio.settings')
django.setup()

# Import the task AFTER django.setup()
from portfolio.tasks import get_chatbot_response

app = FastAPI()

# 2. CORS Settings (Allow traffic from localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/chat")
def run_chat_task(message: str):
    """
    Receives a message, starts a background task, and returns the Task ID.
    """
    task = get_chatbot_response.delay(message)
    return {"task_id": task.id}


@app.get("/api/status/{task_id}")
def get_task_status(task_id: str):
    """
    Checks if the task is finished and returns the result.
    """
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return {"status": "Processing"}
    elif task_result.state == 'SUCCESS':
        return {
            "status": "Done",
            "result": task_result.result
        }
    else:
        return {"status": task_result.state}