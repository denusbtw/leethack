from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from leethack.participations.api.v1.views.mixins import (
    ParticipantFilterMixin,
    ParticipationRequestFilterMixin,
)
from leethack.participations.models import ParticipationRequest, Participant
from leethack.users.api.serializers import (
    MyParticipationRequestListSerializer,
    MyParticipationRequestRetrieveSerializer,
    MyParticipationListSerializer,
)
from .pagination import MyParticipationRequestPagination, MyParticipationPagination


class MyParticipationRequestListAPIView(
    ParticipationRequestFilterMixin, generics.ListAPIView
):
    """
    Returns list of participation requests of request user
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyParticipationRequestListSerializer
    pagination_class = MyParticipationRequestPagination
    search_fields = ("hackathon__title",)

    def get_queryset(self):
        qs = ParticipationRequest.objects.filter(user=self.request.user)
        qs = qs.select_related("hackathon", "hackathon__category")
        return qs


class MyParticipationRequestDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    Returns participation request of request user
    """

    serializer_class = MyParticipationRequestRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ParticipationRequest.objects.filter(user=self.request.user)
        qs = qs.select_related("hackathon", "hackathon__category")
        return qs

    def perform_destroy(self, instance):
        if not instance.is_pending:
            raise PermissionDenied("You can delete only pending requests.")
        instance.delete()


class MyParticipationListAPIView(ParticipantFilterMixin, generics.ListAPIView):
    """
    Returns list of participants where user is current user
    """

    serializer_class = MyParticipationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyParticipationPagination
    search_fields = ("hackathon__title",)

    def get_queryset(self):
        qs = Participant.objects.filter(user=self.request.user)
        qs = qs.select_related("hackathon", "hackathon__category")
        return qs
