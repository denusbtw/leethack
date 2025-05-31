from rest_framework import generics, permissions

from leethack.participations.models import ParticipationRequest, Participant
from leethack.users.api.permissions import CanDeleteOwnParticipationRequest
from leethack.users.api.serializers import (
    MyParticipationRequestListSerializer,
    MyParticipationRequestRetrieveSerializer,
    MyParticipantListSerializer,
)


class MyParticipationRequestListAPIView(generics.ListAPIView):
    """
    Returns list of participation requests of request user
    """

    serializer_class = MyParticipationRequestListSerializer

    def get_queryset(self):
        return ParticipationRequest.objects.filter(user=self.request.user)


class MyParticipationRequestDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    Returns participation request of request user
    """

    serializer_class = MyParticipationRequestRetrieveSerializer

    def get_queryset(self):
        return ParticipationRequest.objects.filter(user=self.request.user)


class MyParticipationListAPIView(generics.ListAPIView):
    """
    Returns list of participants where user is current user
    """

    serializer_class = MyParticipantListSerializer

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user)
