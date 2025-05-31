from rest_framework import serializers

from leethack.participations.api.v1.serializers.nested import (
    ParticipantNestedSerializer,
)
from .nested import CategoryNestedSerializer
from leethack.hackathons.models import Hackathon

from leethack.users.api.serializers import UserNestedSerializer


class BaseHackathonReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    host = UserNestedSerializer()
    title = serializers.CharField()
    category = CategoryNestedSerializer()
    prize = serializers.IntegerField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    winner = ParticipantNestedSerializer()


class HackathonListSerializer(BaseHackathonReadSerializer):
    pass


class HackathonRetrieveSerializer(BaseHackathonReadSerializer):
    description = serializers.CharField()


class HackathonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = (
            "id",
            "title",
            "description",
            "category",
            "prize",
            "start_datetime",
            "end_datetime",
        )


class HackathonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = (
            "title",
            "description",
            "category",
            "prize",
            "start_datetime",
            "end_datetime",
            "winner",
        )
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "category": {"required": False},
            "prize": {"required": False},
            "start_datetime": {"required": False},
            "end_datetime": {"required": False},
        }
