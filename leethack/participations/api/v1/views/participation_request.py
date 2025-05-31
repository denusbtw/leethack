from rest_framework import generics, permissions

from leethack.core.api.permissions import ReadOnly, PostOnly
from leethack.hackathons.api.v1.permissions import IsHackathonHost
from leethack.participations.api.v1.serializers import (
    HackathonParticipationRequestListSerializer,
    HackathonParticipationRequestCreateSerializer,
    HackathonParticipationRequestRetrieveSerializer,
    HackathonParticipationRequestUpdateSerializer,
)
from leethack.participations.models import ParticipationRequest


class HackathonParticipationRequestListCreateAPIView(generics.ListCreateAPIView):
    """
    Returns participation requests of specific hackathon
    """

    permission_classes = [
        ReadOnly & (permissions.IsAdminUser | IsHackathonHost)
        | (PostOnly & permissions.IsAuthenticated)
    ]

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return ParticipationRequest.objects.filter(hackathon_id=hackathon_id)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonParticipationRequestListSerializer
        return HackathonParticipationRequestCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            hackathon_id=self.kwargs["hackathon_id"],
            status=ParticipationRequest.Status.PENDING,
        )


class HackathonParticipationRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns participation request of specific hackathon
    """

    permission_classes = [permissions.IsAdminUser | IsHackathonHost]

    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        return ParticipationRequest.objects.filter(hackathon_id=hackathon_id)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonParticipationRequestRetrieveSerializer
        return HackathonParticipationRequestUpdateSerializer
