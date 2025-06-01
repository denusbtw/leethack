from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied

from leethack.participations.api.v1.filters import ParticipationRequestFilterSet
from leethack.participations.models import ParticipationRequest, Participant
from leethack.users.api.serializers import (
    MyParticipationRequestListSerializer,
    MyParticipationRequestRetrieveSerializer,
    MyParticipationListSerializer,
)
from .pagination import MyParticipationRequestPagination, MyParticipationPagination


class MyParticipationRequestListAPIView(generics.ListAPIView):
    """
    Returns list of participation requests of request user
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyParticipationRequestListSerializer
    pagination_class = MyParticipationRequestPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = ParticipationRequestFilterSet
    search_fields = ("hackathon__title",)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self):
        return ParticipationRequest.objects.filter(user=self.request.user)


class MyParticipationRequestDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    Returns participation request of request user
    """

    serializer_class = MyParticipationRequestRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ParticipationRequest.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        if not instance.is_pending:
            raise PermissionDenied("You can delete only pending requests.")
        instance.delete()


class MyParticipationListAPIView(generics.ListAPIView):
    """
    Returns list of participants where user is current user
    """

    serializer_class = MyParticipationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyParticipationPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ("hackathon__title",)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user)
