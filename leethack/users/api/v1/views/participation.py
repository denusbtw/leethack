from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from leethack.participations.api.v1.views.mixins import (
    ParticipantFilterMixin,
    ParticipationRequestFilterMixin,
)
from leethack.participations.models import ParticipationRequest, Participant
from leethack.users.api.v1.serializers import (
    MyParticipationRequestListSerializer,
    MyParticipationRequestRetrieveSerializer,
    MyParticipationListSerializer,
    MyParticipationRetrieveSerializer,
)
from .pagination import MyParticipationRequestPagination, MyParticipationPagination


class MyParticipationRequestQuerySetMixin:

    def get_queryset(self):
        qs = ParticipationRequest.objects.filter(user=self.request.user)
        qs = qs.select_related("hackathon", "hackathon__category")
        return qs


class MyParticipationQuerySetMixin:

    def get_queryset(self):
        qs = Participant.objects.filter(user=self.request.user)
        qs = qs.select_related("hackathon", "hackathon__category")
        return qs


class MyParticipationRequestListAPIView(
    MyParticipationRequestQuerySetMixin,
    ParticipationRequestFilterMixin,
    generics.ListAPIView,
):
    """
    GET: Return paginated list of participation requests of authenticated user.
    Only authenticated user can perform this action.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyParticipationRequestListSerializer
    pagination_class = MyParticipationRequestPagination
    search_fields = ("hackathon__title",)


class MyParticipationRequestDetailAPIView(
    MyParticipationRequestQuerySetMixin, generics.RetrieveDestroyAPIView
):
    """
    GET: Return detailed information about specific participation request of authenticated user.
    DELETE: Delete participation request (only pending).
    Only authenticated user can perform these actions.
    """

    serializer_class = MyParticipationRequestRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if not instance.is_pending:
            raise PermissionDenied("You can delete only pending requests.")
        instance.delete()


class MyParticipationListAPIView(
    MyParticipationQuerySetMixin, ParticipantFilterMixin, generics.ListAPIView
):
    """
    GET: Return paginated list of hackathons the authenticated user is participating in.
    Only authenticated user can perform this action.
    """

    serializer_class = MyParticipationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyParticipationPagination
    search_fields = ("hackathon__title",)


class MyParticipationDetailAPIView(
    MyParticipationQuerySetMixin, generics.RetrieveDestroyAPIView
):
    """
    GET: Return detailed information about participant of authenticated user in hackathons.
    DELETE: Delete participant.
    Only authenticated user can perform these actions.
    """

    serializer_class = MyParticipationRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]
