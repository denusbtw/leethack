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
    GET: Return a paginated list of participant for a specific hackathon.
    Only hackathon host or admin can perform this action.
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
    GET: Retrieve detailed information about specific participant of specific hackathon.
    DELETE: Delete a participant of a specific hackathon.
    Only hackathon host or admin can perform these actions.
    """

    serializer_class = HackathonParticipantDetailSerializer
    permission_classes = [IsHackathonHost | (ReadOnly & permissions.IsAdminUser)]
