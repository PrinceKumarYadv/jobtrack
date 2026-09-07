"""
Server-rendered "shell" pages for the JobTrack UI.

These views only render the HTML skeleton (navbar, layout, empty tables,
forms, etc). All real data comes from the DRF API via JavaScript `fetch()`
calls using the JWT access token stored in the browser's localStorage
(see static/js/app.js). Pages that require a logged-in user perform that
check client-side and redirect to /login/ if no valid token is present -
this keeps the authentication story in one place (the API) while still
letting the project use plain Django templates, as required by the stack.
"""

from django.views.generic import TemplateView


class LoginPageView(TemplateView):
    template_name = "login.html"


class RegisterPageView(TemplateView):
    template_name = "register.html"


class DashboardPageView(TemplateView):
    template_name = "dashboard.html"


class ApplicationsPageView(TemplateView):
    template_name = "applications.html"


class ApplicationFormPageView(TemplateView):
    template_name = "application_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = kwargs.get("pk")
        return context


class ApplicationDetailPageView(TemplateView):
    template_name = "application_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_id"] = kwargs.get("pk")
        return context


class InterviewsPageView(TemplateView):
    template_name = "interviews.html"


class InterviewFormPageView(TemplateView):
    template_name = "interview_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interview_id"] = kwargs.get("pk")
        context["application_id"] = self.request.GET.get("application")
        return context


class ProfilePageView(TemplateView):
    template_name = "profile.html"
