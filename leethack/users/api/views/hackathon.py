from rest_framework import generics, permissions

from leethack.hackathons.api.v1.serializers import HackathonListSerializer
from leethack.hackathons.api.v1.views.mixins import HackathonFilterMixin
from leethack.hackathons.models import Hackathon
from .pagination import (
    MyParticipatedHackathonPagination,
    MyHostedHackathonPagination,
    UserHostedHackathonPagination,
)


class HackathonSelectRelatedQuerySetMixin:
    def get_queryset(self):
        return Hackathon.objects.select_related(
            "category", "host", "winner", "winner__user"
        )


class MyParticipatedHackathonListAPIView(
    HackathonSelectRelatedQuerySetMixin, HackathonFilterMixin, generics.ListAPIView
):
    """
    GET: Return paginated list of hackathons the authenticated user is participating in.
    Only authenticated user can perform this action.
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyParticipatedHackathonPagination

    def get_queryset(self):
        return super().get_queryset().filter(participants__user=self.request.user)


class MyHostedHackathonListAPIView(
    HackathonSelectRelatedQuerySetMixin, HackathonFilterMixin, generics.ListAPIView
):
    """
    GET: Return paginated list of hackathons the authenticated user is hosting.
    Only host can perform this action.
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyHostedHackathonPagination

    def get_queryset(self):
        return super().get_queryset().filter(host=self.request.user)


class UserHostedHackathonListAPIView(
    HackathonSelectRelatedQuerySetMixin, HackathonFilterMixin, generics.ListAPIView
):
    """
    GET: Return paginated list of hackathons the specific user is hosting.
    Any user can perform this action.
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = UserHostedHackathonPagination

    def get_queryset(self):
        return super().get_queryset().filter(host_id=self.kwargs["user_id"])
