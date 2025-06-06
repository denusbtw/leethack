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
from leethack.participations.models import ParticipationRequest, Participant


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
    GET: Return list of pagination participation requests for a specific hackathon. Only hackathon host or admin can perform this action.
    POST: Create pending participation request for current user. Only authenticated user can perform this action.
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["hackathon_id"] = self.kwargs["hackathon_id"]
        return context

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
    GET: Return detailed information about specific participation request.
    PATCH: Update only status (approved or rejected) of participation request.
    DELETE: Delete participation request.
    Only hackathon host or admin can perform these actions.
    """

    permission_classes = [permissions.IsAdminUser | IsHackathonHost]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonParticipationRequestRetrieveSerializer
        return HackathonParticipationRequestUpdateSerializer
