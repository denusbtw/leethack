from rest_framework import serializers

from leethack.hackathons.api.v1.serializers.nested import HackathonNestedSerializer


class BaseMyParticipationRequestReadSerializer(serializers.Serializer):
    """Base read serializer for ParticipationRequest model"""

    id = serializers.UUIDField(help_text="Unique identifier of participation request.")
    hackathon = HackathonNestedSerializer(
        help_text="Nested detailed representation of hackathon."
    )
    status = serializers.CharField(
        source="get_status_display",
        help_text="Human-readable status of participation request.",
    )
    created_at = serializers.DateTimeField(
        help_text="Timestamp when the participation request was created."
    )
    updated_at = serializers.DateTimeField(
        help_text="Timestamp when the participation request was last updated."
    )


class MyParticipationRequestListSerializer(BaseMyParticipationRequestReadSerializer):
    """Serializer for listing participation requests of authenticated user."""

    pass


class MyParticipationRequestRetrieveSerializer(
    BaseMyParticipationRequestReadSerializer
):
    """Serializer for retrieving detailed information about participation request of authenticated user."""

    pass


class MyParticipationListSerializer(serializers.Serializer):
    """Serializer for listing Participant instances where authenticated user is participating in."""

    id = serializers.UUIDField(help_text="Unique identifier of participant.")
    hackathon = HackathonNestedSerializer(
        help_text="Nested detailed representation of hackathon."
    )
    created_at = serializers.DateTimeField(
        help_text="Timestamp when the participation record was created."
    )
