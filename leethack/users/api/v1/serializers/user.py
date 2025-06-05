from django.conf import settings
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from leethack.core.utils import build_image_validators

User = get_user_model()


class UserNestedSerializer(serializers.Serializer):
    """Nested serializer for User model."""

    id = serializers.UUIDField(help_text="Unique identifier of user.")
    username = serializers.CharField(help_text="Username of user.")
    email = serializers.EmailField(help_text="Email of user.")
    profile_picture = serializers.ImageField(
        help_text="URL of profile picture stored in Cloudflare R2."
    )


class MeRetrieveSerializer(serializers.Serializer):
    """Serializer for retrieving detailed information about authenticated user."""

    id = serializers.UUIDField(help_text="Unique identifier of user.")
    username = serializers.CharField(help_text="Username of user.")
    email = serializers.EmailField(help_text="Email of user.")
    first_name = serializers.CharField(help_text="First name of user.")
    last_name = serializers.CharField(help_text="Last name of user.")
    profile_picture = serializers.ImageField(
        help_text="URL of profile picture stored in Cloudflare R2."
    )
    profile_background = serializers.ImageField(
        help_text="URL of profile background stored in Cloudflare R2."
    )


class MeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating authenticated user.
    Validates profile picture, profile background and password
    """

    profile_picture = serializers.ImageField(
        validators=build_image_validators(settings.PROFILE_PICTURE_CONFIG),
        required=False,
        help_text="New profile picture.",
    )
    profile_background = serializers.ImageField(
        validators=build_image_validators(settings.PROFILE_BACKGROUND_CONFIG),
        required=False,
        help_text="New profile background.",
    )
    password = serializers.CharField(
        write_only=True, required=False, min_length=8, help_text="New password."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile_picture",
            "profile_background",
        )
        extra_kwargs = {
            "email": {"required": False},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
