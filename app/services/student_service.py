from sqlmodel import Session
from fastapi import HTTPException
from app.repository.student_repository import StudentRepository


class StudentService:

    def __init__(self):
        self.repo = StudentRepository()

    def create_student(self, session: Session, data):
        return self.repo.create(session, data)

    def get_students(self, session: Session):
        return self.repo.get_all(session)

    def get_student(self, session: Session, student_id: int):
        student = self.repo.get_by_id(session, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def delete_student(self, session: Session, student_id: int):
        student = self.repo.delete(session, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Deleted successfully"}