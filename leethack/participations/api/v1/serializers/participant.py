from rest_framework import serializers

from leethack.users.api.serializers import UserNestedSerializer


class BaseHackathonParticipantReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserNestedSerializer()
    created_at = serializers.DateTimeField()


class HackathonParticipantListSerializer(BaseHackathonParticipantReadSerializer):
    pass


class HackathonParticipantDetailSerializer(BaseHackathonParticipantReadSerializer):
    pass
