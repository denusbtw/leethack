import pytest
from django.db import IntegrityError

from leethack.participations.models import Participant


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

    @pytest.mark.parametrize(
        "participation_request_fixture, should_pass",
        [
            ("approved_participation_request", True),
            ("pending_participation_request", False),
            ("rejected_participation_request", False),
        ],
    )
    def test_is_approved(self, participation_request_fixture, should_pass, request):
        participation_request = request.getfixturevalue(participation_request_fixture)
        assert participation_request.is_approved == should_pass

    @pytest.mark.parametrize(
        "participation_request_fixture, should_pass",
        [
            ("approved_participation_request", False),
            ("pending_participation_request", True),
            ("rejected_participation_request", False),
        ],
    )
    def test_is_pending(self, participation_request_fixture, should_pass, request):
        participation_request = request.getfixturevalue(participation_request_fixture)
        assert participation_request.is_pending == should_pass

    @pytest.mark.parametrize(
        "participation_request_fixture, should_pass",
        [
            ("approved_participation_request", False),
            ("pending_participation_request", False),
            ("rejected_participation_request", True),
        ],
    )
    def test_is_rejected(self, participation_request_fixture, should_pass, request):
        participation_request = request.getfixturevalue(participation_request_fixture)
        assert participation_request.is_rejected == should_pass

    def test_approve_sets_approved_status(self, pending_participation_request):
        pending_participation_request.approve()
        assert pending_participation_request.is_approved

    def test_approve_creates_participant(self, pending_participation_request):
        user = pending_participation_request.user
        hackathon = pending_participation_request.hackathon

        pending_participation_request.approve()
        assert Participant.objects.filter(user=user, hackathon=hackathon).exists()

    def test_reject_sets_rejected_status(self, pending_participation_request):
        pending_participation_request.reject()
        assert pending_participation_request.is_rejected

    def test_reject_deletes_participant_if_request_was_approved(
        self, approved_participation_request, participant_factory
    ):
        user = approved_participation_request.user
        hackathon = approved_participation_request.hackathon
        participant = participant_factory(user=user, hackathon=hackathon)

        approved_participation_request.reject()
        assert approved_participation_request.is_rejected
        assert not Participant.objects.filter(pk=participant.pk).exists()
