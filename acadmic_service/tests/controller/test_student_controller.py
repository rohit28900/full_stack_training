from unittest.mock import patch

from app.models.student_model import Student


class TestStudentController:

    @patch(
        "app.controller.student_controller.student_service.create_student"
    )
    def test_create_student(
        self,
        mock_create_student,
        client
    ):

        mock_create_student.return_value = Student(
            id=1,
            name="Rohit",
            email="rohit@test.com",
            age=25
        )

        payload = {
            "name": "Rohit",
            "email": "rohit@test.com",
            "age": 25
        }

        response = client.post(
            "/students/",
            json=payload
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Rohit"

    @patch(
        "app.controller.student_controller.student_service.get_students"
    )
    def test_get_students(
        self,
        mock_get_students,
        client
    ):

        mock_get_students.return_value = [
            {
                "id": 1,
                "name": "Rohit",
                "email": "rohit@test.com",
                "age": 25
            }
        ]

        response = client.get("/students/")

        assert response.status_code == 200
        assert len(response.json()) == 1

    @patch(
        "app.controller.student_controller.student_service.get_student"
    )
    def test_get_student_by_id(
        self,
        mock_get_student,
        client
    ):

        mock_get_student.return_value = {
            "id": 1,
            "name": "Rohit",
            "email": "rohit@test.com",
            "age": 25
        }

        response = client.get("/students/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1

    @patch(
        "app.controller.student_controller.student_service.delete_student"
    )
    def test_delete_student(
        self,
        mock_delete_student,
        client
    ):

        mock_delete_student.return_value = {
            "message": "Deleted successfully"
        }

        response = client.delete("/students/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Deleted successfully"