from datetime import date

from rest_framework import serializers

from companies.models import Company
from companies.serializers import CompanySerializer
from interviews.models import Interview
from .models import JobApplication


class InterviewInlineSerializer(serializers.ModelSerializer):
    """Lightweight interview representation nested inside an application."""

    class Meta:
        model = Interview
        fields = [
            "id", "interview_date", "interview_time", "interview_type",
            "interviewer", "meeting_link", "notes", "result", "created_at",
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Full read/write serializer for job applications.

    Accepts `company_name` (plus optional website/location/industry) on
    write, and returns a nested `company` object on read - this keeps the
    "Add Application" form simple (just type the company name) while still
    modelling companies as their own table.
    """

    company = CompanySerializer(read_only=True)
    company_name = serializers.CharField(write_only=True)
    company_website = serializers.URLField(write_only=True, required=False, allow_blank=True)
    company_location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    company_industry = serializers.CharField(write_only=True, required=False, allow_blank=True)
    interviews = InterviewInlineSerializer(many=True, read_only=True)
    status_badge_class = serializers.CharField(read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id", "company", "company_name", "company_website", "company_location", "company_industry",
            "job_title", "job_type", "location", "salary", "job_url", "application_date",
            "status", "priority", "notes", "created_at", "updated_at",
            "interviews", "status_badge_class",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_job_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Job title is required.")
        return value.strip()

    def validate_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_application_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Application date cannot be in the future.")
        return value

    def _get_or_create_company(self, validated_data):
        name = validated_data.pop("company_name").strip()
        website = validated_data.pop("company_website", "") or ""
        location = validated_data.pop("company_location", "") or ""
        industry = validated_data.pop("company_industry", "") or ""

        company, created = Company.objects.get_or_create(
            company_name__iexact=name,
            defaults={
                "company_name": name,
                "website": website,
                "location": location,
                "industry": industry,
            },
        )
        return company

    def create(self, validated_data):
        company = self._get_or_create_company(validated_data)
        validated_data["company"] = company
        validated_data["user"] = self.context["request"].user
        return JobApplication.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "company_name" in validated_data:
            company = self._get_or_create_company(validated_data)
            instance.company = company
        else:
            for field in ("company_website", "company_location", "company_industry"):
                validated_data.pop(field, None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class JobApplicationListSerializer(serializers.ModelSerializer):
    """Slimmer serializer used for the applications list/table view."""

    company_name = serializers.CharField(source="company.company_name", read_only=True)
    status_badge_class = serializers.CharField(read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id", "company_name", "job_title", "location", "job_type",
            "application_date", "status", "priority", "status_badge_class",
        ]
