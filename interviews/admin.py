from django.contrib import admin

from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = [
        "application", "interview_date", "interview_time",
        "interview_type", "interviewer", "result",
    ]
    list_filter = ["interview_type", "result", "interview_date"]
    search_fields = ["application__job_title", "application__company__company_name", "interviewer"]
    ordering = ["interview_date", "interview_time"]
    date_hierarchy = "interview_date"
    raw_id_fields = ["application"]
