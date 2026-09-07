from django.db import models

from applications.models import JobApplication


class Interview(models.Model):
    """An interview round scheduled for a specific job application."""

    class InterviewType(models.TextChoices):
        PHONE = "Phone", "Phone"
        VIDEO = "Video", "Video"
        TECHNICAL = "Technical", "Technical"
        HR = "HR", "HR"
        ONSITE = "Onsite", "Onsite"

    class Result(models.TextChoices):
        PENDING = "Pending", "Pending"
        PASSED = "Passed", "Passed"
        FAILED = "Failed", "Failed"

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    interview_date = models.DateField()
    interview_time = models.TimeField()
    interview_type = models.CharField(max_length=20, choices=InterviewType.choices, default=InterviewType.VIDEO)
    interviewer = models.CharField(max_length=150, blank=True)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    result = models.CharField(max_length=10, choices=Result.choices, default=Result.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["interview_date", "interview_time"]
        indexes = [
            models.Index(fields=["interview_date"]),
        ]

    def __str__(self):
        return f"{self.application.job_title} interview on {self.interview_date}"
