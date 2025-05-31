import pytest
from rest_framework import serializers

from leethack.hackathons.api.v1.serializers import HackathonUpdateSerializer


@pytest.mark.django_db
class TestHackathonUpdateSerializer:

    def test_error_if_trying_to_set_winner_on_active_hackathon(
        self, participant_factory, hackathon_factory, future_date, past_date
    ):
        hackathon = hackathon_factory(
            start_datetime=past_date, end_datetime=future_date
        )
        participant = participant_factory(hackathon=hackathon)

        data = {"winner": participant.pk}
        serializer = HackathonUpdateSerializer(hackathon, data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_error_if_trying_to_set_winner_not_participant_of_hackathon(
        self, participant_factory, hackathon_factory, past_date, future_date
    ):
        hackathon = hackathon_factory(
            start_datetime=past_date, end_datetime=future_date
        )

        winner = participant_factory()
        data = {"winner": winner.pk}

        serializer = HackathonUpdateSerializer(hackathon, data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
