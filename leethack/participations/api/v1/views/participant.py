from rest_framework import generics, permissions

from leethack.core.api.permissions import ReadOnly
from leethack.hackathons.api.v1.permissions import IsHackathonHost
from ..serializers import (
    HackathonParticipantListSerializer,
    HackathonParticipantDetailSerializer,
)
from leethack.participations.models import Participant


class HackathonParticipantListAPIView(generics.ListAPIView):
    """
    Returns all participants of specific hackathon
    """

    serializer_class = HackathonParticipantListSerializer
    permission_classes = [permissions.IsAdminUser | IsHackathonHost]

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return Participant.objects.filter(hackathon_id=hackathon_id)


class HackathonParticipantDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    Returns participant of specific hackathon
    """

    serializer_class = HackathonParticipantDetailSerializer
    permission_classes = [IsHackathonHost | (ReadOnly & permissions.IsAdminUser)]

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return Participant.objects.filter(hackathon_id=hackathon_id)
