from django.db import models


class Company(models.Model):
    """A company that a user has applied to. Shared across all users."""

    company_name = models.CharField(max_length=200, db_index=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["company_name"]
        verbose_name_plural = "Companies"
        constraints = [
            models.UniqueConstraint(fields=["company_name"], name="unique_company_name")
        ]

    def __str__(self):
        return self.company_name
