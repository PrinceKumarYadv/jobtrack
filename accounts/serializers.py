from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user registration with password confirmation."""

    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "password", "confirm_password", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name is required.")
        return value.strip()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    """Validates email/password credentials for login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Used for viewing and updating the logged-in user's profile."""

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_email(self, value):
        value = value.lower().strip()
        qs = User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None)
        if qs.exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Used for changing the logged-in user's password."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})
        return attrs
