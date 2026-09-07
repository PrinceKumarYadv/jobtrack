from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name", "website", "location", "industry", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_company_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Company name is required.")
        return value.strip()
