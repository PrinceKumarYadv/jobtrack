from datetime import date

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import JobApplication
from interviews.models import Interview


class DashboardView(APIView):
    """
    GET /api/dashboard/

    Returns aggregated, user-specific statistics used to power the
    dashboard cards, charts, "upcoming interviews" and "recent applications"
    widgets. All data is scoped to the logged-in user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        applications = JobApplication.objects.filter(user=user)

        status_counts = {
            row["status"]: row["count"]
            for row in applications.values("status").annotate(count=Count("id"))
        }

        status_breakdown = [
            {"status": choice_value, "count": status_counts.get(choice_value, 0)}
            for choice_value, _ in JobApplication.Status.choices
        ]

        monthly_qs = (
            applications
            .annotate(month=TruncMonth("application_date"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        applications_over_time = [
            {"month": row["month"].strftime("%b %Y"), "count": row["count"]}
            for row in monthly_qs if row["month"] is not None
        ]

        upcoming_interviews_qs = (
            Interview.objects.filter(
                application__user=user,
                interview_date__gte=timezone.localdate(),
            )
            .select_related("application", "application__company")
            .order_by("interview_date", "interview_time")[:10]
        )
        upcoming_interviews = [
            {
                "id": interview.id,
                "company_name": interview.application.company.company_name,
                "job_title": interview.application.job_title,
                "interview_date": interview.interview_date,
                "interview_time": interview.interview_time,
                "interview_type": interview.interview_type,
                "meeting_link": interview.meeting_link,
            }
            for interview in upcoming_interviews_qs
        ]

        recent_applications_qs = applications.select_related("company").order_by("-created_at")[:5]
        recent_applications = [
            {
                "id": app.id,
                "company_name": app.company.company_name,
                "job_title": app.job_title,
                "status": app.status,
                "application_date": app.application_date,
            }
            for app in recent_applications_qs
        ]

        data = {
            "total_applications": applications.count(),
            "applied": status_counts.get("Applied", 0),
            "shortlisted": status_counts.get("Shortlisted", 0),
            "interview": status_counts.get("Interview", 0),
            "selected": status_counts.get("Selected", 0),
            "rejected": status_counts.get("Rejected", 0),
            "withdrawn": status_counts.get("Withdrawn", 0),
            "status_breakdown": status_breakdown,
            "applications_over_time": applications_over_time,
            "upcoming_interviews": upcoming_interviews,
            "recent_applications": recent_applications,
        }
        return Response(data)
