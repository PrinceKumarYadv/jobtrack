from rest_framework import viewsets, permissions

from .filters import JobApplicationFilter
from .models import JobApplication
from .serializers import JobApplicationSerializer, JobApplicationListSerializer


class IsOwner(permissions.BasePermission):
    """Object-level permission: only the owning user may access an application."""

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for job applications, scoped strictly to the logged-in user.

    Supports:
      GET    /api/applications/               (list, paginated)
      POST   /api/applications/               (create)
      GET    /api/applications/<id>/          (detail)
      PUT    /api/applications/<id>/          (full update)
      PATCH  /api/applications/<id>/          (partial update)
      DELETE /api/applications/<id>/          (delete)

    Filtering & search:
      ?status=Interview&job_type=Internship&priority=High
      ?search=python   (matches job_title, company name, location)
      ?ordering=-application_date
    """

    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_class = JobApplicationFilter
    search_fields = ["job_title", "company__company_name", "location"]
    ordering_fields = ["application_date", "created_at", "job_title", "priority", "status"]
    ordering = ["-application_date"]

    def get_queryset(self):
        # A user must never see another user's applications.
        return (
            JobApplication.objects.filter(user=self.request.user)
            .select_related("company")
            .prefetch_related("interviews")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return JobApplicationListSerializer
        return JobApplicationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
