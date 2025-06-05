from rest_framework import serializers

from leethack.hackathons.api.v1.serializers.nested import HackathonNestedSerializer
from leethack.users.api.serializers import UserNestedSerializer


class ParticipantNestedSerializer(serializers.Serializer):
    """Nested serializer for Participant model."""

    id = serializers.UUIDField(help_text="Unique identifier of participant.")
    user = UserNestedSerializer(help_text="Nested detailed representation of user.")
    hackathon = HackathonNestedSerializer(
        help_text="Nested detailed representation of hackathon."
    )
