from rest_framework import serializers

from leethack.hackathons.api.v1.serializers.nested import HackathonNestedSerializer


class BaseMyParticipationRequestReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    hackathon = HackathonNestedSerializer()
    status = serializers.CharField(source="get_status_display")
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class MyParticipationRequestListSerializer(serializers.Serializer):
    pass


class MyParticipationRequestRetrieveSerializer(serializers.Serializer):
    pass


class MyParticipationListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    hackathon = HackathonNestedSerializer()
    created_at = serializers.DateTimeField()
