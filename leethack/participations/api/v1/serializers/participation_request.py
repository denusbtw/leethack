from django.db import transaction
from rest_framework import serializers

from leethack.hackathons.api.v1.serializers.nested import HackathonNestedSerializer
from leethack.participations.models import ParticipationRequest
from leethack.users.api.serializers import UserNestedSerializer


class BaseHackathonParticipationRequestReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserNestedSerializer()
    hackathon = HackathonNestedSerializer()
    status = serializers.CharField(source="get_status_display")
    created_at = serializers.DateTimeField()


class HackathonParticipationRequestListSerializer(
    BaseHackathonParticipationRequestReadSerializer
):
    pass


class HackathonParticipationRequestRetrieveSerializer(
    BaseHackathonParticipationRequestReadSerializer
):
    pass


class HackathonParticipationRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationRequest
        fields = ("id",)


class HackathonParticipationRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationRequest
        fields = ("status",)

    def validate_status(self, value):
        allowed_statuses = {
            ParticipationRequest.Status.APPROVED,
            ParticipationRequest.Status.REJECTED,
        }

        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value

    def update(self, instance, validated_data):
        status = validated_data.pop("status")

        with transaction.atomic():
            if status == ParticipationRequest.Status.APPROVED:
                instance.approve()
            elif status == ParticipationRequest.Status.REJECTED:
                instance.reject()
            else:
                raise serializers.ValidationError("Unsupported status update.")

        return instance
