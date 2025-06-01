from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..filters import HackathonFilterSet


class HackathonFilterMixin:
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_class = HackathonFilterSet
    # TODO: move search in description in SearchVector
    search_fields = ("title", "description")
    ordering_fields = ("start_datetime", "end_datetime", "prize")
