from typing import Optional
from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # ORM -> Schema erlauben
