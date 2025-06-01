from django_filters import rest_framework as filters

from leethack.participations.models import ParticipationRequest


class ParticipationRequestFilterSet(filters.FilterSet):
    status = filters.MultipleChoiceFilter(choices=ParticipationRequest.Status.choices)

    class Meta:
        model = ParticipationRequest
        fields = ("status",)
