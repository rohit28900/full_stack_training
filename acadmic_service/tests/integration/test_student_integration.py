from unittest.mock import Mock

import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_session

from app.models.student_model import Student

from app.controller.student_controller import get_user



class TestStudentIntegration:

    # -----------------------------
    # CREATE STUDENT
    # -----------------------------
    def test_create_student(
        self,
        client,
        mock_session
    ):

        def refresh(student):
            student.id = 1

        mock_session.refresh.side_effect = refresh

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

        data = response.json()

        assert data["id"] == 1
        assert data["name"] == "Rohit"

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    # -----------------------------
    # GET ALL STUDENTS
    # -----------------------------
    def test_get_students(
        self,
        client,
        mock_session
    ):

        students = [
            Student(
                id=1,
                name="Rohit",
                email="rohit@test.com",
                age=25
            )
        ]

        mock_exec = Mock()

        mock_exec.all.return_value = students

        mock_session.exec.return_value = mock_exec

        response = client.get(
            "/students/"
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["name"] == "Rohit"

    # -----------------------------
    # GET STUDENT BY ID
    # -----------------------------
    def test_get_student_by_id(
        self,
        client,
        mock_session
    ):

        student = Student(
            id=1,
            name="Virat",
            email="virat@test.com",
            age=30
        )

        mock_session.get.return_value = student

        response = client.get(
            "/students/1"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 1
        assert data["name"] == "Virat"

    # -----------------------------
    # DELETE STUDENT
    # -----------------------------
    def test_delete_student(
        self,
        client,
        mock_session
    ):

        student = Student(
            id=1,
            name="Delete User",
            email="delete@test.com",
            age=22
        )

        mock_session.get.return_value = student

        response = client.delete(
            "/students/1"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "Deleted successfully"

        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()