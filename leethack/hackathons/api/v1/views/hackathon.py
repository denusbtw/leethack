from rest_framework import generics, permissions, filters

from leethack.core.api.permissions import ReadOnly
from ..permissions import IsHackathonHost
from ..serializers import (
    HackathonListSerializer,
    HackathonCreateSerializer,
    HackathonRetrieveSerializer,
    HackathonUpdateSerializer,
)
from .pagination import HackathonPagination
from leethack.hackathons.models import Hackathon
from leethack.users.api.permissions import IsHost


class HackathonListCreateAPIView(generics.ListCreateAPIView):
    """
    Returns list of all hackathons
    """

    queryset = Hackathon.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHost]
    pagination_class = HackathonPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # TODO: move search in description in SearchVector
    search_fields = ("title", "description")
    ordering_fields = ("start_datetime", "end_datetime", "prize")
    ordering = ["start_datetime"]
    # TODO: create HackathonFilterSet

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonListSerializer
        return HackathonCreateSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class HackathonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns hackathon
    """

    queryset = Hackathon.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHackathonHost]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HackathonRetrieveSerializer
        return HackathonUpdateSerializer

    def get_hackathon_id(self):
        return self.kwargs["pk"]
