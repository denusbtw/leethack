from rest_framework import generics, permissions

from leethack.core.api.permissions import ReadOnly
from ..permissions import IsHackathonHost
from ..serializers import (
    HackathonListSerializer,
    HackathonCreateSerializer,
    HackathonRetrieveSerializer,
    HackathonUpdateSerializer,
)
from leethack.hackathons.models import Hackathon
from leethack.users.api.permissions import IsHost


class HackathonListCreateAPIView(generics.ListCreateAPIView):
    """
    Returns list of all hackathons
    """

    queryset = Hackathon.objects.all()
    permission_classes = [ReadOnly | permissions.IsAdminUser | IsHost]

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
