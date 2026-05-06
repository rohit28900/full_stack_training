from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.student_schema import StudentCreate, StudentResponse
from app.services.student_service import StudentService
from common_auth.common_auth.rbac import has_permission
from common_auth.common_auth.auth import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/students", tags=["Students"])

student_service = StudentService()
get_user = get_current_user(settings)


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, session: Session = Depends(get_session),
                   user=Depends(has_permission("user.create", get_user))):
    return student_service.create_student(session, student)


@router.get("/", response_model=List[StudentResponse])
def get_students(session: Session = Depends(get_session),
                 user=Depends(has_permission("user.read", get_user))):
    return student_service.get_students(session)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, session: Session = Depends(get_session),
               user=Depends(has_permission("user.read", get_user))):
    return student_service.get_student(session, student_id)


@router.delete("/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session),
                   user=Depends(has_permission("user.delete", get_user))):
    return student_service.delete_student(session, student_id)