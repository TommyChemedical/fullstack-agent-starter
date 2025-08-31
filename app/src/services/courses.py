from typing import List, Optional
from sqlalchemy.orm import Session
from app.src.models.course import Course
from app.src.schemas.course import CourseCreate

def create_course(db: Session, data: CourseCreate) -> Course:
    obj = Course(title=data.title, description=data.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_courses(db: Session) -> List[Course]:
    return db.query(Course).order_by(Course.id.asc()).all()

def get_course(db: Session, course_id: int) -> Optional[Course]:
    return db.get(Course, course_id)
