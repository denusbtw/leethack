from django.conf import settings
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from leethack.core.utils import build_image_validators

User = get_user_model()


class UserNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
    profile_picture = serializers.ImageField()


class MeRetrieveSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_picture = serializers.ImageField()
    profile_background = serializers.ImageField()


class MeUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        validators=build_image_validators(settings.PROFILE_PICTURE_CONFIG),
        required=False,
    )
    profile_background = serializers.ImageField(
        validators=build_image_validators(settings.PROFILE_BACKGROUND_CONFIG),
        required=False,
    )
    password = serializers.CharField(write_only=True, required=False, min_length=8)

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
