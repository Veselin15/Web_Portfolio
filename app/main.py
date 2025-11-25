from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import chat, projects  # Import our routers

app = FastAPI(title="Professional Portfolio")

# Mount Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Templates
templates = Jinja2Templates(directory="app/templates")

# --- INCLUDE ROUTERS (This connects your "urls" folders) ---
app.include_router(chat.router)
app.include_router(projects.router)

@app.get("/")
async def home(request: Request):
    """
    Renders the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})