import pytest
from django.db import IntegrityError


@pytest.mark.django_db
class TestParticipant:

    def test_error_if_not_unique_user_and_hackathon(
        self, user_factory, hackathon_factory, participant_factory
    ):
        user = user_factory()
        hackathon = hackathon_factory()

        participant = participant_factory(user=user, hackathon=hackathon)
        with pytest.raises(IntegrityError):
            participant_factory(user=user, hackathon=hackathon)


@pytest.mark.django_db
class TestParticipationRequest:

    def test_error_if_not_unique_user_and_hackathon(
        self, user_factory, hackathon_factory, participation_request_factory
    ):
        user = user_factory()
        hackathon = hackathon_factory()

        participation_request = participation_request_factory(
            user=user, hackathon=hackathon
        )
        with pytest.raises(IntegrityError):
            participation_request_factory(user=user, hackathon=hackathon)
