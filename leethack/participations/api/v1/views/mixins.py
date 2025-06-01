from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..filters import ParticipationRequestFilterSet


class ParticipantFilterMixin:
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)


class ParticipationRequestFilterMixin:
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = ParticipationRequestFilterSet
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)
