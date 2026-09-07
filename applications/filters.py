import django_filters

from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):
    """
    Supports:
      /api/applications/?status=Interview
      /api/applications/?job_type=Internship
      /api/applications/?priority=High
      /api/applications/?date_from=2026-01-01&date_to=2026-02-01
    Combine any of the above with ?search=... (handled by SearchFilter).
    """

    status = django_filters.ChoiceFilter(choices=JobApplication.Status.choices)
    job_type = django_filters.ChoiceFilter(choices=JobApplication.JobType.choices)
    priority = django_filters.ChoiceFilter(choices=JobApplication.Priority.choices)
    date_from = django_filters.DateFilter(field_name="application_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="application_date", lookup_expr="lte")

    class Meta:
        model = JobApplication
        fields = ["status", "job_type", "priority", "date_from", "date_to"]
