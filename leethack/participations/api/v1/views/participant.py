from rest_framework import generics

from ..serializers import (
    HackathonParticipantListSerializer,
    HackathonParticipantDetailSerializer,
)
from leethack.participations.models import Participant


class HackathonParticipantListAPIView(generics.ListAPIView):
    serializer_class = HackathonParticipantListSerializer

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return Participant.objects.filter(hackathon_id=hackathon_id)


class HackathonParticipantDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = HackathonParticipantDetailSerializer

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return Participant.objects.filter(hackathon_id=hackathon_id)
