import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def list_url(hackathon):
    return reverse(
        "api:v1:hackathon_participant_list", kwargs={"hackathon_id": hackathon.pk}
    )


@pytest.mark.django_db
class TestHackathonParticipantListAPIView:

    def test_lists_only_participants_of_specific_hackathon(
        self, api_client, list_url, hackathon, participant_factory
    ):
        participant_factory.create_batch(2, hackathon=hackathon)
        participant_factory.create_batch(3)

        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
