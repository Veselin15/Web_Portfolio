from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get DB URL from environment variables, defaulting to a local fallback if missing
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://myuser:mypassword@localhost/portfolio_db")

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base class for our models
Base = declarative_base()

# Dependency to get DB session in endpoints
async def get_db():
    async with SessionLocal() as session:
        yield session