from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from celery.result import AsyncResult
from .tasks import ai_response_task

app = FastAPI()

# Mount static files (CSS, JS, Images) if you need them later
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates directory (similar to Django templates)
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root(request: Request):
    """
    Renders the homepage.
    We pass the 'request' object required by Jinja2.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_bot(name: str):
    """
    Starts a background task with Celery.
    Returns the task ID immediately so the UI doesn't freeze.
    """
    task = ai_response_task.delay(name)
    return {"task_id": task.id, "message": "Task started"}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    """
    Checks the status of the Celery task.
    The frontend polls this endpoint until the status is 'Done'.
    """
    res = AsyncResult(task_id)
    if res.ready():
        return {"status": "Done", "result": res.result}
    return {"status": "Processing"}