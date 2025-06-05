from rest_framework import generics, permissions

from leethack.core.api.permissions import ReadOnly
from .mixins import HackathonFilterMixin
from ..permissions import IsHackathonHost
from ..serializers import (
    HackathonListSerializer,
    HackathonCreateSerializer,
    HackathonRetrieveSerializer,
    HackathonUpdateSerializer,
)
from .pagination import HackathonPagination
from leethack.hackathons.models import Hackathon
from leethack.users.api.v1.permissions import IsHost


class HackathonQuerySetMixin:
    def get_queryset(self):
        return Hackathon.objects.select_related("category", "host", "winner")


class HackathonListCreateAPIView(
    HackathonQuerySetMixin, HackathonFilterMixin, generics.ListCreateAPIView
):
    """
    GET: Return paginated list of hackathons.
    POST: Create new hackathon.
    Only hosts or admin can perform these actions.
    """

    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHost]
    pagination_class = HackathonPagination
    ordering = ("start_datetime",)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonListSerializer
        return HackathonCreateSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class HackathonDetailAPIView(
    HackathonQuerySetMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    GET: Retrieve detailed information about a specific hackathon.
    PATCH: Update hackathon details.
    DELETE: Delete a hackathon..
    Only hackathon host or admin can perform these actions.
    """

    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHackathonHost]

    def get_queryset(self):
        return super().get_queryset().select_related("winner__user")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonRetrieveSerializer
        return HackathonUpdateSerializer

    def get_hackathon_id(self):
        return self.kwargs["pk"]
