from rest_framework import generics, permissions, filters

from leethack.core.api.permissions import ReadOnly, PostOnly
from leethack.hackathons.api.v1.permissions import IsHackathonHost
from .mixins import ParticipationRequestFilterMixin
from .pagination import HackathonParticipationRequestPagination
from ..serializers import (
    HackathonParticipationRequestListSerializer,
    HackathonParticipationRequestCreateSerializer,
    HackathonParticipationRequestRetrieveSerializer,
    HackathonParticipationRequestUpdateSerializer,
)
from leethack.participations.models import ParticipationRequest


class HackathonParticipationRequestQuerySetMixin:
    def get_queryset(self):
        hackathon_id = self.kwargs["hackathon_id"]
        qs = ParticipationRequest.objects.filter(hackathon_id=hackathon_id)
        qs = qs.select_related("user")
        return qs


class HackathonParticipationRequestListCreateAPIView(
    HackathonParticipationRequestQuerySetMixin,
    ParticipationRequestFilterMixin,
    generics.ListCreateAPIView,
):
    """
    Returns participation requests of specific hackathon
    """

    permission_classes = [
        ReadOnly & (permissions.IsAdminUser | IsHackathonHost)
        | (PostOnly & permissions.IsAuthenticated)
    ]
    pagination_class = HackathonParticipationRequestPagination
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

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


class HackathonParticipationRequestDetailAPIView(
    HackathonParticipationRequestQuerySetMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Returns participation request of specific hackathon
    """

    permission_classes = [permissions.IsAdminUser | IsHackathonHost]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonParticipationRequestRetrieveSerializer
        return HackathonParticipationRequestUpdateSerializer
