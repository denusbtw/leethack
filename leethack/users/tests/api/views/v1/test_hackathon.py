import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def my_participated_hackathon_list_url():
    return reverse("api:v1:my_participated_hackathon_list")


@pytest.fixture
def my_hosted_hackathon_list_url():
    return reverse("api:v1:my_hosted_hackathon_list")


@pytest.fixture
def user_hosted_hackathon_list(host):
    return reverse("api:v1:user_hosted_hackathon_list", kwargs={"user_id": host.pk})


@pytest.mark.django_db
class TestMyParticipatedHackathonListAPIView:

    def test_lists_only_hackathons_participated_by_request_user(
        self, api_client, my_participated_hackathon_list_url, user, participant_factory
    ):
        api_client.force_authenticate(user=user)
        participant_factory.create_batch(2, user=user)
        participant_factory.create_batch(3)

        response = api_client.get(my_participated_hackathon_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestMyHostedHackathonListAPIView:

    def test_lists_only_hackathons_hosted_by_request_user(
        self, api_client, my_hosted_hackathon_list_url, host, hackathon_factory
    ):
        api_client.force_authenticate(user=host)

        hackathon_factory.create_batch(2, host=host)
        hackathon_factory.create_batch(3)

        response = api_client.get(my_hosted_hackathon_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestUserHostedHackathonListAPIView:

    def test_lists_only_hackathons_hosted_by_specific_user(
        self, api_client, user_hosted_hackathon_list, host, hackathon_factory
    ):
        hackathon_factory.create_batch(2, host=host)
        hackathon_factory.create_batch(3)

        response = api_client.get(user_hosted_hackathon_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
