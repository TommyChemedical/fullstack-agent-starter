from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.src.core.database import get_session
from app.src.schemas.course import CourseCreate, CourseOut
from app.src.services.courses import create_course, list_courses, get_course

router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.post("", response_model=CourseOut, status_code=201)
def create(data: CourseCreate, db: Session = Depends(get_session)):
    return create_course(db, data)

@router.get("", response_model=List[CourseOut])
def list_(db: Session = Depends(get_session)):
    return list_courses(db)

@router.get("/{course_id}", response_model=CourseOut)
def get_(course_id: int, db: Session = Depends(get_session)):
    obj = get_course(db, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj
