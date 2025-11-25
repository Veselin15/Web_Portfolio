import time
from .worker import celery_app

@celery_app.task
def ai_response_task(name: str):
    time.sleep(5)  # Simulation
    return f"Hello, {name}! This is a asynchronous bot answer."