from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, LogoutView, ProfileView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="api-register"),
    path("login/", LoginView.as_view(), name="api-login"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="api-token-refresh"),
    path("profile/", ProfileView.as_view(), name="api-profile"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="api-change-password"),
]
