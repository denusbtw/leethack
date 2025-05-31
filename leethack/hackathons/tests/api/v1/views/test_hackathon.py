import pytest
from django.urls import reverse
from rest_framework import status

from leethack.hackathons.models import Hackathon


@pytest.fixture
def list_url():
    return reverse("api:v1:hackathon_list")


@pytest.fixture
def detail_url(hackathon):
    return reverse("api:v1:hackathon_detail", kwargs={"pk": hackathon.pk})


@pytest.fixture
def data(category_factory, past_date, future_date):
    category = category_factory()
    return {
        "title": "test hackathon",
        "description": "test decsription",
        "category": category.pk,
        "prize": 1000,
        "start_datetime": past_date,
        "end_datetime": future_date,
    }


@pytest.mark.django_db
class TestHackathonListCreateAPIView:

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_anonymous_user(
            self, api_client, list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_authenticated_user(
            self, api_client, list_url, user, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(list_url, data=data)
            assert response.status_code == expected_status_code

    def test_perform_create_sets_host(self, api_client, list_url, host, data):
        api_client.force_authenticate(user=host)
        response = api_client.post(list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        hackathon = Hackathon.objects.get(pk=response.data["id"])
        assert hackathon.host == host


@pytest.mark.django_db
class TestHackathonDetailAPIView:
    pass
