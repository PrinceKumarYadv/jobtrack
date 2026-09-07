from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class RegisterView(generics.CreateAPIView):
    """POST /api/register/ -- Create a new user account."""

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = _tokens_for_user(user)
        return Response(
            {
                "detail": "Account created successfully.",
                "user": UserProfileSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/login/ -- Authenticate a user and issue JWT tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = _tokens_for_user(user)
        return Response(
            {
                "detail": "Login successful.",
                "user": UserProfileSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    POST /api/logout/ -- Blacklist/invalidate the supplied refresh token.

    Since token blacklisting is optional, this endpoint simply validates the
    refresh token was well-formed; the client is responsible for discarding
    the stored tokens. This still gives a clean, explicit logout endpoint.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() if hasattr(token, "blacklist") else None
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/profile/ -- View or update the logged-in user's profile."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """POST /api/profile/change-password/ -- Change the logged-in user's password."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
