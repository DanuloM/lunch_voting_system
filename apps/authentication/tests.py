from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "role": "employee"
        }
        response = self.client.post("/api/v1/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["role"], "employee")

    def test_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="pass123")
        data = {
            "username": "testuser",
            "password": "testpass123",
            "role": "employee"
        }
        response = self.client.post("/api/v1/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="employee"
        )
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "wrongpass"
        }
        response = self.client.post("/api/v1/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_endpoint(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="employee"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_create_employee_as_admin(self):
        admin = User.objects.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        self.client.force_authenticate(user=admin)
        data = {
            "username": "newemployee",
            "password": "emp123"
        }
        response = self.client.post("/api/v1/auth/employees/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newemployee", role="employee").exists())

    def test_create_employee_as_non_admin(self):
        employee = User.objects.create_user(
            username="employee",
            password="emp123",
            role="employee"
        )
        self.client.force_authenticate(user=employee)
        data = {
            "username": "newemployee",
            "password": "emp123"
        }
        response = self.client.post("/api/v1/auth/employees/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_employees_as_admin(self):
        admin = User.objects.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        User.objects.create_user(username="emp1", password="pass", role="employee")
        User.objects.create_user(username="emp2", password="pass", role="employee")
        self.client.force_authenticate(user=admin)
        response = self.client.get("/api/v1/auth/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
