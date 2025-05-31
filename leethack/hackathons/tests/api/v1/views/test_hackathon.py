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
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_default_user(
            self, api_client, list_url, user, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_host(
            self, api_client, list_url, host, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=host)
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

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_anonymous_user(
            self, api_client, detail_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_default_user(
            self, api_client, detail_url, user, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_host_but_not_hackathon_host(
            self, api_client, detail_url, hackathon, host, method, expected_status_code
        ):
            assert hackathon.host != host
            api_client.force_authenticate(user=host)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_200_OK),
                ("patch", status.HTTP_200_OK),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_hackathon_host(
            self, api_client, detail_url, hackathon, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.host)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_200_OK),
                ("patch", status.HTTP_200_OK),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_admin_user(
            self, api_client, detail_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code
