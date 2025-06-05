from django.utils import timezone
from django_filters import rest_framework as filters

from leethack.hackathons.models import Hackathon


class HackathonFilterSet(filters.FilterSet):
    """
    FilterSet for filtering Hackathon queryset.
    """

    category = filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    hackathon_status = filters.CharFilter(method="filter_status")
    start_after = filters.DateTimeFilter(field_name="start_datetime", lookup_expr="gte")
    end_before = filters.DateTimeFilter(field_name="end_datetime", lookup_expr="lte")
    winner = filters.CharFilter(method="filter_winner")

    class Meta:
        model = Hackathon
        fields = ("category", "hackathon_status", "start_after", "end_before", "winner")

    def filter_status(self, queryset, name, value):
        now = timezone.now()

        match value:
            case "active":
                return queryset.filter(start_datetime__lte=now, end_datetime__gte=now)
            case "past":
                return queryset.filter(end_datetime__lte=now)
            case _:
                return queryset

    def filter_winner(self, queryset, name, value):
        qs = queryset.exclude(winner__isnull=True)
        qs = qs.filter(winner__user__username=value)
        return qs
