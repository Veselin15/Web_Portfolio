from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Project(Base):
    """
    Database model representing a portfolio project.
    This class maps directly to the 'projects' table in PostgreSQL.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # The name of the project
    description = Column(Text)          # Longer text description
    image_url = Column(String, nullable=True) # URL to a screenshot/image
    link_url = Column(String, nullable=True)  # Link to the live project or GitHub