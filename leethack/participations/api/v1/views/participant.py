from rest_framework import generics, permissions

from leethack.core.api.permissions import ReadOnly
from leethack.hackathons.api.v1.permissions import IsHackathonHost
from .mixins import ParticipantFilterMixin
from ..serializers import (
    HackathonParticipantListSerializer,
    HackathonParticipantDetailSerializer,
)
from .pagination import HackathonParticipantPagination
from leethack.participations.models import Participant


class HackathonParticipantQuerySetMixin:
    def get_queryset(self):
        qs = Participant.objects.filter(hackathon_id=self.kwargs["hackathon_id"])
        qs = qs.select_related("user")
        return qs


class HackathonParticipantListAPIView(
    HackathonParticipantQuerySetMixin, ParticipantFilterMixin, generics.ListAPIView
):
    """
    Returns all participants of specific hackathon
    """

    serializer_class = HackathonParticipantListSerializer
    permission_classes = [permissions.IsAdminUser | IsHackathonHost]
    pagination_class = HackathonParticipantPagination
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )


class HackathonParticipantDetailAPIView(
    HackathonParticipantQuerySetMixin, generics.RetrieveDestroyAPIView
):
    """
    Returns participant of specific hackathon
    """

    serializer_class = HackathonParticipantDetailSerializer
    permission_classes = [IsHackathonHost | (ReadOnly & permissions.IsAdminUser)]
