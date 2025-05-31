import pytest
from django.urls import reverse
from rest_framework import status

from leethack.participations.models import ParticipationRequest


@pytest.fixture
def list_url(hackathon):
    return reverse(
        "api:v1:hackathon_participation_request_list",
        kwargs={"hackathon_id": hackathon.pk},
    )


@pytest.mark.django_db
class TestHackathonParticipationRequestListCreateAPIView:

    def test_lists_participation_requests_only_of_specific_hackathon(
        self, api_client, list_url, hackathon, participation_request_factory
    ):
        participation_request_factory.create_batch(2, hackathon=hackathon)
        participation_request_factory.create_batch(3)

        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_perform_create_sets_user_and_hackathon(
        self, api_client, list_url, hackathon, user
    ):
        api_client.force_authenticate(user=user)
        response = api_client.post(list_url)
        assert response.status_code == status.HTTP_201_CREATED

        participation_request = ParticipationRequest.objects.get(pk=response.data["id"])
        assert participation_request.user == user
        assert participation_request.hackathon == hackathon
