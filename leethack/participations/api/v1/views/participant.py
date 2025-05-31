from rest_framework import generics, permissions, filters

from leethack.core.api.permissions import ReadOnly
from leethack.hackathons.api.v1.permissions import IsHackathonHost
from ..serializers import (
    HackathonParticipantListSerializer,
    HackathonParticipantDetailSerializer,
)
from .pagination import HackathonParticipantPagination
from leethack.participations.models import Participant


class HackathonParticipantListAPIView(generics.ListAPIView):
    """
    Returns all participants of specific hackathon
    """

    serializer_class = HackathonParticipantListSerializer
    permission_classes = [permissions.IsAdminUser | IsHackathonHost]
    pagination_class = HackathonParticipantPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

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
