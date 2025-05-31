from rest_framework import serializers

from leethack.hackathons.api.v1.serializers.nested import HackathonNestedSerializer
from leethack.users.api.serializers import UserNestedSerializer


class ParticipantNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserNestedSerializer()
    hackathon = HackathonNestedSerializer()
