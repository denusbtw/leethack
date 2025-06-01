from rest_framework import serializers

from django.contrib.auth import get_user_model

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
            "password": {"required": False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
