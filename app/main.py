from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import chat, projects
from app.core.database import engine, Base
from app.models import project as project_model

# --- NEW IMPORTS FOR ADMIN ---
from sqladmin import Admin, ModelView
# -----------------------------

app = FastAPI(title="Professional Portfolio")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(chat.router)
app.include_router(projects.router)

# --- 1. SETUP ADMIN PANEL ---
admin = Admin(app, engine)

# --- 2. REGISTER MODELS ---
class ProjectAdmin(ModelView, model=project_model.Project):
    column_list = [project_model.Project.id, project_model.Project.title]

admin.add_view(ProjectAdmin)
# --------------------------

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})