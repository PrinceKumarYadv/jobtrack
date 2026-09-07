from rest_framework import serializers


class StatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    count = serializers.IntegerField()


class UpcomingInterviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company_name = serializers.CharField()
    job_title = serializers.CharField()
    interview_date = serializers.DateField()
    interview_time = serializers.TimeField()
    interview_type = serializers.CharField()
    meeting_link = serializers.CharField(allow_blank=True)


class RecentApplicationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company_name = serializers.CharField()
    job_title = serializers.CharField()
    status = serializers.CharField()
    application_date = serializers.DateField()


class DashboardSerializer(serializers.Serializer):
    """Documents the shape returned by GET /api/dashboard/."""

    total_applications = serializers.IntegerField()
    applied = serializers.IntegerField()
    shortlisted = serializers.IntegerField()
    interview = serializers.IntegerField()
    selected = serializers.IntegerField()
    rejected = serializers.IntegerField()
    withdrawn = serializers.IntegerField()
    status_breakdown = StatusCountSerializer(many=True)
    applications_over_time = MonthlyCountSerializer(many=True)
    upcoming_interviews = UpcomingInterviewSerializer(many=True)
    recent_applications = RecentApplicationSerializer(many=True)
