from sqlmodel import Session, select
from app.models.student_model import Student


class StudentRepository:

    def create(self, session: Session, data):
        student = Student(**data.model_dump())
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

    def get_all(self, session: Session):
        return session.exec(select(Student)).all()

    def get_by_id(self, session: Session, student_id: int):
        return session.get(Student, student_id)

    def delete(self, session: Session, student_id: int):
        student = session.get(Student, student_id)
        if student:
            session.delete(student)
            session.commit()
        return student