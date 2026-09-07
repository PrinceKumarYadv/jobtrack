from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "job_title", "company", "user", "job_type", "status",
        "priority", "application_date", "created_at",
    ]
    list_filter = ["status", "job_type", "priority", "application_date"]
    search_fields = ["job_title", "company__company_name", "user__email", "location"]
    ordering = ["-application_date"]
    date_hierarchy = "application_date"
    autocomplete_fields = ["company"]
    raw_id_fields = ["user"]
