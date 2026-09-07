from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["company_name", "industry", "location", "website", "created_at"]
    list_filter = ["industry"]
    search_fields = ["company_name", "location", "industry"]
    ordering = ["company_name"]
