from app.models.student_model import Student
from app.repository.student_repository import StudentRepository
from app.schemas.student_schema import StudentCreate


class TestStudentRepository:

    def test_create_student(
        self,
        mock_session
    ):

        repo = StudentRepository()

        payload = StudentCreate(
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        result = repo.create(
            mock_session,
            payload
        )

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

        assert result.name == "Rohit"

    def test_get_by_id(
        self,
        mock_session
    ):

        repo = StudentRepository()

        student = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        mock_session.get.return_value = student

        result = repo.get_by_id(
            mock_session,
            1
        )

        assert result.id == 1

    def test_delete_student(
        self,
        mock_session
    ):

        repo = StudentRepository()

        student = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        mock_session.get.return_value = student

        result = repo.delete(
            mock_session,
            1
        )

        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()

        assert result.id == 1