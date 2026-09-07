from datetime import date, time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from applications.models import JobApplication
from companies.models import Company
from .models import Interview


class InterviewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="owner@example.com", full_name="Owner", password="StrongPass123")
        self.other_user = User.objects.create_user(email="other@example.com", full_name="Other", password="StrongPass123")
        self.company = Company.objects.create(company_name="TestCo")
        self.application = JobApplication.objects.create(
            user=self.user, company=self.company, job_title="Developer",
            job_type="Full Time", application_date=date(2026, 1, 1), status="Interview",
        )
        self.other_application = JobApplication.objects.create(
            user=self.other_user, company=self.company, job_title="Other Role",
            job_type="Full Time", application_date=date(2026, 1, 1), status="Interview",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_interview(self):
        url = reverse("interview-list")
        payload = {
            "application": self.application.id,
            "interview_date": "2026-02-01",
            "interview_time": "10:00:00",
            "interview_type": "Technical",
            "interviewer": "Alex",
            "result": "Pending",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interview.objects.filter(application=self.application).count(), 1)

    def test_cannot_create_interview_for_other_users_application(self):
        url = reverse("interview-list")
        payload = {
            "application": self.other_application.id,
            "interview_date": "2026-02-01",
            "interview_time": "10:00:00",
            "interview_type": "Technical",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_interviews(self):
        Interview.objects.create(
            application=self.application, interview_date=date(2026, 2, 1),
            interview_time=time(10, 0), interview_type="Video",
        )
        Interview.objects.create(
            application=self.other_application, interview_date=date(2026, 2, 1),
            interview_time=time(10, 0), interview_type="Video",
        )
        response = self.client.get(reverse("interview-list"))
        self.assertEqual(response.data["count"], 1)

    def test_cannot_access_other_users_interview(self):
        other_interview = Interview.objects.create(
            application=self.other_application, interview_date=date(2026, 2, 1),
            interview_time=time(10, 0), interview_type="Video",
        )
        response = self.client.get(reverse("interview-detail", args=[other_interview.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_interview(self):
        interview = Interview.objects.create(
            application=self.application, interview_date=date(2026, 2, 1),
            interview_time=time(10, 0), interview_type="Video",
        )
        response = self.client.delete(reverse("interview-detail", args=[interview.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
