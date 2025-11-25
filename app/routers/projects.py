from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

# Create a router for portfolio projects
router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    # Here we will later query the database
    return [{"name": "Project 1"}, {"name": "Project 2"}]