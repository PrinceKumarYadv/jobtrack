from django.conf import settings
from django.db import models

from companies.models import Company


class JobApplication(models.Model):
    """A single job application belonging to one user."""

    class JobType(models.TextChoices):
        FULL_TIME = "Full Time", "Full Time"
        PART_TIME = "Part Time", "Part Time"
        INTERNSHIP = "Internship", "Internship"
        CONTRACT = "Contract", "Contract"
        REMOTE = "Remote", "Remote"

    class Status(models.TextChoices):
        APPLIED = "Applied", "Applied"
        SHORTLISTED = "Shortlisted", "Shortlisted"
        INTERVIEW = "Interview", "Interview"
        SELECTED = "Selected", "Selected"
        REJECTED = "Rejected", "Rejected"
        WITHDRAWN = "Withdrawn", "Withdrawn"

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job_title = models.CharField(max_length=200, db_index=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    location = models.CharField(max_length=200, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    job_url = models.URLField(blank=True)
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED, db_index=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-application_date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "application_date"]),
        ]

    def __str__(self):
        return f"{self.job_title} @ {self.company.company_name} ({self.status})"

    STATUS_BADGE_CLASSES = {
        "Applied": "badge-status-applied",
        "Shortlisted": "badge-status-shortlisted",
        "Interview": "badge-status-interview",
        "Selected": "badge-status-selected",
        "Rejected": "badge-status-rejected",
        "Withdrawn": "badge-status-withdrawn",
    }

    @property
    def status_badge_class(self):
        return self.STATUS_BADGE_CLASSES.get(self.status, "badge-secondary")
