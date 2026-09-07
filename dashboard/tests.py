from datetime import date, time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from applications.models import JobApplication
from companies.models import Company
from interviews.models import Interview


class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="dash@example.com", full_name="Dash User", password="StrongPass123")
        self.company = Company.objects.create(company_name="TestCo")
        self.client.force_authenticate(user=self.user)

    def test_dashboard_counts(self):
        JobApplication.objects.create(
            user=self.user, company=self.company, job_title="Role A",
            job_type="Full Time", application_date=date(2026, 1, 1), status="Applied",
        )
        interview_app = JobApplication.objects.create(
            user=self.user, company=self.company, job_title="Role B",
            job_type="Full Time", application_date=date(2026, 1, 5), status="Interview",
        )
        Interview.objects.create(
            application=interview_app, interview_date=date(2026, 12, 31),
            interview_time=time(10, 0), interview_type="Video",
        )

        response = self.client.get(reverse("api-dashboard"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_applications"], 2)
        self.assertEqual(response.data["applied"], 1)
        self.assertEqual(response.data["interview"], 1)
        self.assertEqual(len(response.data["recent_applications"]), 2)

    def test_dashboard_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("api-dashboard"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_scoped_to_user(self):
        other_user = User.objects.create_user(email="other2@example.com", full_name="Other", password="StrongPass123")
        JobApplication.objects.create(
            user=other_user, company=self.company, job_title="Not Mine",
            job_type="Full Time", application_date=date(2026, 1, 1), status="Applied",
        )
        response = self.client.get(reverse("api-dashboard"))
        self.assertEqual(response.data["total_applications"], 0)
