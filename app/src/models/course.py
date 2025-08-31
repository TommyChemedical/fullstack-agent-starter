from sqlalchemy import Column, Integer, String, Text
from app.src.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
