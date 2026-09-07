from rest_framework import viewsets, permissions

from .models import Interview
from .serializers import InterviewSerializer


class IsInterviewOwner(permissions.BasePermission):
    """Object-level permission: only the owner of the related application may act on it."""

    def has_object_permission(self, request, view, obj):
        return obj.application.user_id == request.user.id


class InterviewViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for interviews, scoped to interviews on the logged-in user's
    own applications.

      GET    /api/interviews/
      POST   /api/interviews/
      GET    /api/interviews/<id>/
      PUT    /api/interviews/<id>/
      DELETE /api/interviews/<id>/
    """

    permission_classes = [permissions.IsAuthenticated, IsInterviewOwner]
    serializer_class = InterviewSerializer
    ordering_fields = ["interview_date", "interview_time", "result"]
    ordering = ["interview_date"]

    def get_queryset(self):
        return (
            Interview.objects.filter(application__user=self.request.user)
            .select_related("application", "application__company")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
