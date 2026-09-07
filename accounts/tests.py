from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistrationTests(APITestCase):
    def test_register_success(self):
        url = reverse("api-register")
        payload = {
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="jane@example.com").exists())
        self.assertIn("access", response.data["tokens"])

    def test_register_password_mismatch(self):
        url = reverse("api-register")
        payload = {
            "full_name": "Jane Doe",
            "email": "jane2@example.com",
            "password": "StrongPass123",
            "confirm_password": "DifferentPass123",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        User.objects.create_user(email="dupe@example.com", full_name="Existing", password="StrongPass123")
        url = reverse("api-register")
        payload = {
            "full_name": "New User",
            "email": "dupe@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        url = reverse("api-register")
        payload = {
            "full_name": "Jane Doe",
            "email": "short@example.com",
            "password": "short1",
            "confirm_password": "short1",
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="login@example.com", full_name="Login User", password="StrongPass123")

    def test_login_success(self):
        url = reverse("api-login")
        response = self.client.post(url, {"email": "login@example.com", "password": "StrongPass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])

    def test_login_invalid_credentials(self):
        url = reverse("api-login")
        response = self.client.post(url, {"email": "login@example.com", "password": "WrongPass"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="profile@example.com", full_name="Profile User", password="StrongPass123")
        self.client.force_authenticate(user=self.user)

    def test_view_profile(self):
        response = self.client.get(reverse("api-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "profile@example.com")

    def test_update_profile(self):
        response = self.client.put(reverse("api-profile"), {"full_name": "Updated Name", "email": "profile@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Name")

    def test_change_password(self):
        response = self.client.post(reverse("api-change-password"), {
            "old_password": "StrongPass123",
            "new_password": "NewStrongPass123",
            "confirm_new_password": "NewStrongPass123",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPass123"))

    def test_change_password_wrong_old_password(self):
        response = self.client.post(reverse("api-change-password"), {
            "old_password": "WrongOldPass",
            "new_password": "NewStrongPass123",
            "confirm_new_password": "NewStrongPass123",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("api-profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
