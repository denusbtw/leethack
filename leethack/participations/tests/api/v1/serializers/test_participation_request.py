import pytest
from rest_framework import serializers

from leethack.participations.api.v1.serializers.participation_request import (
    HackathonParticipationRequestUpdateSerializer,
)
from leethack.participations.models import ParticipationRequest


# @pytest.mark.django_db
# class TestHackathonParticipationRequestUpdateSerializer:
#
#     def test_error_if_status_not_allowed(self, participation_request):
#         data = {"status": ParticipationRequest.Status.PENDING}
#         serializer = HackathonParticipationRequestUpdateSerializer(
#             participation_request, data
#         )
#
#         with pytest.raises(serializers.ValidationError):
#             serializer.is_valid(raise_exception=True)
