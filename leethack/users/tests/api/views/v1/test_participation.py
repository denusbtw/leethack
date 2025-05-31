import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def my_participation_request_list_url():
    return reverse("api:v1:my_participation_request_list")


@pytest.fixture
def participation_request(participation_request_factory):
    return participation_request_factory()


@pytest.fixture
def my_participation_request_detail_url(participation_request):
    return reverse(
        "api:v1:my_participation_request_detail",
        kwargs={"pk": participation_request.pk},
    )


@pytest.fixture
def my_participation_list_url():
    return reverse("api:v1:my_participation_list")


@pytest.mark.django_db
class TestMyParticipationRequestListAPIView:

    def test_lists_only_participation_requests_of_request_user(
        self,
        api_client,
        my_participation_request_list_url,
        user,
        participation_request_factory,
    ):
        participation_request_factory.create_batch(2, user=user)
        participation_request_factory.create_batch(3)

        api_client.force_authenticate(user=user)
        response = api_client.get(my_participation_request_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.django_db
class TestMyParticipationRequestDetailAPIView:
    pass


@pytest.mark.django_db
class TestMyParticipationListAPIView:

    def test_lists_only_participants_of_request_user(
        self, api_client, my_participation_list_url, user, participant_factory
    ):
        participant_factory.create_batch(2, user=user)
        participant_factory.create_batch(3)

        api_client.force_authenticate(user=user)
        response = api_client.get(my_participation_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
