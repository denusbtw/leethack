from django.db import transaction
from rest_framework import serializers

from leethack.participations.models import ParticipationRequest, Participant
from leethack.users.api.v1.serializers import UserNestedSerializer


class BaseHackathonParticipationRequestReadSerializer(serializers.Serializer):
    """Base read serializer for participation requests of hackathon."""

    id = serializers.UUIDField(help_text="Unique identifier of participation request.")
    user = UserNestedSerializer(help_text="Nested detail information about user.")
    status = serializers.CharField(
        source="get_status_display",
        help_text="Human-readable status of participation request.",
    )
    created_at = serializers.DateTimeField(
        help_text="Timestamp when the participation request was created."
    )


class HackathonParticipationRequestListSerializer(
    BaseHackathonParticipationRequestReadSerializer
):
    """Serializer for listing participation requests"""

    pass


class HackathonParticipationRequestRetrieveSerializer(
    BaseHackathonParticipationRequestReadSerializer
):
    """Serializer for retrieving detailed information about participation request."""

    pass


class HackathonParticipationRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating pending participation request of hackathon."""

    class Meta:
        model = ParticipationRequest
        fields = ("id",)

    def validate(self, attrs):
        user = self.context["request"].user
        hackathon_id = self.context["hackathon_id"]

        if Participant.objects.filter(user=user, hackathon_id=hackathon_id).exists():
            raise serializers.ValidationError(
                "User is already participant of this hackathon."
            )

        return attrs


class HackathonParticipationRequestUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating status of participation request."""

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
