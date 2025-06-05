from rest_framework import serializers

from leethack.users.api.serializers import UserNestedSerializer


class BaseHackathonParticipantReadSerializer(serializers.Serializer):
    """Base read serializer for participants of hackathon."""

    id = serializers.UUIDField(help_text="Unique identifier of participant.")
    user = UserNestedSerializer(help_text="Nested detail representation of user.")
    created_at = serializers.DateTimeField(
        help_text="Timestamp when the participant record was created."
    )


class HackathonParticipantListSerializer(BaseHackathonParticipantReadSerializer):
    """Serializer for listing participants."""

    pass


class HackathonParticipantDetailSerializer(BaseHackathonParticipantReadSerializer):
    """Serializer for retrieving detailed information about participant."""

    pass
