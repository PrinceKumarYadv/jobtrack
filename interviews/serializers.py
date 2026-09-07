from datetime import date

from rest_framework import serializers

from applications.models import JobApplication
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    """
    Full interview serializer.

    `application` accepts the JobApplication id on write and is restricted
    (in the view) to applications owned by the requesting user, so a user
    can never attach an interview to someone else's application.
    """

    company_name = serializers.CharField(source="application.company.company_name", read_only=True)
    job_title = serializers.CharField(source="application.job_title", read_only=True)

    class Meta:
        model = Interview
        fields = [
            "id", "application", "company_name", "job_title",
            "interview_date", "interview_time", "interview_type",
            "interviewer", "meeting_link", "notes", "result", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_application(self, value):
        request = self.context["request"]
        if value.user_id != request.user.id:
            raise serializers.ValidationError("You do not have access to this application.")
        return value
