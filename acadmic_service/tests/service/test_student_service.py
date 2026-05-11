from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.services.student_service import StudentService
from app.models.student_model import Student


class TestStudentService:

    @patch("app.services.student_service.StudentRepository")
    def test_create_student(
        self,
        mock_repo_class
    ):

        # mock repo object
        mock_repo = mock_repo_class.return_value

        # fake session
        mock_session = Mock()

        # fake input data
        mock_data = Mock()

        # fake student
        mock_student = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        # repo response
        mock_repo.create.return_value = mock_student

        # service object
        service = StudentService()

        result = service.create_student(
            mock_session,
            mock_data
        )

        assert result.id == 1
        assert result.name == "Rohit"

        mock_repo.create.assert_called_once_with(
            mock_session,
            mock_data
        )

    @patch("app.services.student_service.StudentRepository")
    def test_get_students(
        self,
        mock_repo_class
    ):

        mock_repo = mock_repo_class.return_value

        mock_session = Mock()

        mock_students = [
            Student(
                id=1,
                name="Rohit",
                email="rohit@test.com",
                age=25
            )
        ]

        mock_repo.get_all.return_value = mock_students

        service = StudentService()

        result = service.get_students(mock_session)

        assert len(result) == 1
        assert result[0].name == "Rohit"

    @patch("app.services.student_service.StudentRepository")
    def test_get_student_success(
        self,
        mock_repo_class
    ):

        mock_repo = mock_repo_class.return_value

        mock_session = Mock()

        mock_student = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        mock_repo.get_by_id.return_value = mock_student

        service = StudentService()

        result = service.get_student(
            mock_session,
            1
        )

        assert result.id == 1

    @patch("app.services.student_service.StudentRepository")
    def test_get_student_not_found(
        self,
        mock_repo_class
    ):

        mock_repo = mock_repo_class.return_value

        mock_session = Mock()

        mock_repo.get_by_id.return_value = None

        service = StudentService()

        with pytest.raises(HTTPException) as exc:

            service.get_student(
                mock_session,
                1
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Student not found"

    @patch("app.services.student_service.StudentRepository")
    def test_delete_student_success(
        self,
        mock_repo_class
    ):

        mock_repo = mock_repo_class.return_value

        mock_session = Mock()

        mock_student = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        mock_repo.delete.return_value = mock_student

        service = StudentService()

        result = service.delete_student(
            mock_session,
            1
        )

        assert result == {
            "message": "Deleted successfully"
        }

    @patch("app.services.student_service.StudentRepository")
    def test_delete_student_not_found(
        self,
        mock_repo_class
    ):

        mock_repo = mock_repo_class.return_value

        mock_session = Mock()

        mock_repo.delete.return_value = None

        service = StudentService()

        with pytest.raises(HTTPException) as exc:

            service.delete_student(
                mock_session,
                1
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Student not found"