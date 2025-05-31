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
