from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("", views.DashboardPageView.as_view(), name="dashboard"),
    path("applications/", views.ApplicationsPageView.as_view(), name="applications"),
    path("applications/add/", views.ApplicationFormPageView.as_view(), name="application-add"),
    path("applications/<int:pk>/", views.ApplicationDetailPageView.as_view(), name="application-detail-page"),
    path("applications/<int:pk>/edit/", views.ApplicationFormPageView.as_view(), name="application-edit"),
    path("interviews/", views.InterviewsPageView.as_view(), name="interviews"),
    path("interviews/add/", views.InterviewFormPageView.as_view(), name="interview-add"),
    path("interviews/<int:pk>/edit/", views.InterviewFormPageView.as_view(), name="interview-edit"),
    path("profile/", views.ProfilePageView.as_view(), name="profile"),
]
