from django_filters import rest_framework as filters

from leethack.participations.models import ParticipationRequest


class ParticipationRequestFilterSet(filters.FilterSet):
    """FilterSet for ParticipationRequest model."""

    status = filters.MultipleChoiceFilter(choices=ParticipationRequest.Status.choices)

    class Meta:
        model = ParticipationRequest
        fields = ("status",)
