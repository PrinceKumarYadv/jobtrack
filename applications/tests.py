from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from companies.models import Company
from .models import JobApplication


class JobApplicationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="owner@example.com", full_name="Owner", password="StrongPass123")
        self.other_user = User.objects.create_user(email="other@example.com", full_name="Other", password="StrongPass123")
        self.client.force_authenticate(user=self.user)

    def _create_application(self, user=None, **overrides):
        company = Company.objects.create(company_name=overrides.pop("company_name", "TestCo"))
        data = {
            "user": user or self.user,
            "company": company,
            "job_title": "Software Engineer",
            "job_type": JobApplication.JobType.FULL_TIME,
            "application_date": date(2026, 1, 1),
            "status": JobApplication.Status.APPLIED,
            "priority": JobApplication.Priority.MEDIUM,
        }
        data.update(overrides)
        return JobApplication.objects.create(**data)

    def test_create_application(self):
        url = reverse("application-list")
        payload = {
            "company_name": "Amazon",
            "job_title": "Backend Developer",
            "job_type": "Full Time",
            "location": "Bengaluru",
            "salary": "800000.00",
            "job_url": "https://amazon.jobs/1",
            "application_date": "2026-01-15",
            "status": "Applied",
            "priority": "High",
            "notes": "Referred by a friend.",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.filter(user=self.user).count(), 1)
        self.assertEqual(response.data["company"]["company_name"], "Amazon")

    def test_create_application_requires_job_title(self):
        url = reverse("application-list")
        payload = {
            "company_name": "Amazon",
            "job_title": "   ",
            "job_type": "Full Time",
            "application_date": "2026-01-15",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_future_application_date_rejected(self):
        url = reverse("application-list")
        payload = {
            "company_name": "Amazon",
            "job_title": "Backend Developer",
            "job_type": "Full Time",
            "application_date": "2099-01-01",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_returns_own_applications(self):
        self._create_application()
        self._create_application(user=self.other_user, company_name="OtherCo")

        response = self.client.get(reverse("application-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_cannot_view_other_users_application(self):
        other_app = self._create_application(user=self.other_user, company_name="OtherCo")
        response = self.client.get(reverse("application-detail", args=[other_app.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_application(self):
        application = self._create_application()
        url = reverse("application-detail", args=[application.id])
        payload = {
            "company_name": "TestCo",
            "job_title": "Senior Software Engineer",
            "job_type": "Full Time",
            "application_date": "2026-01-01",
            "status": "Interview",
            "priority": "High",
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        application.refresh_from_db()
        self.assertEqual(application.status, "Interview")

    def test_delete_application(self):
        application = self._create_application()
        url = reverse("application-detail", args=[application.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobApplication.objects.filter(id=application.id).exists())

    def test_filter_by_status(self):
        self._create_application(status="Applied", company_name="A")
        self._create_application(status="Interview", company_name="B")

        response = self.client.get(reverse("application-list"), {"status": "Interview"})
        self.assertEqual(response.data["count"], 1)

    def test_search_by_job_title(self):
        self._create_application(job_title="Python Developer", company_name="A")
        self._create_application(job_title="Java Developer", company_name="B")

        response = self.client.get(reverse("application-list"), {"search": "Python"})
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("application-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
