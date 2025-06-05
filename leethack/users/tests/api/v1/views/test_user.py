import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def me_detail_url():
    return reverse("api:v1:me_detail")


@pytest.mark.django_db
class TestMeDetailAPIView:

    def test_returns_request_user(self, api_client, me_detail_url, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(me_detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(user.id)

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_403_FORBIDDEN),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_anonymous_user(
            self, api_client, me_detail_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(me_detail_url)
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
        def test_authenticated_user(
            self, api_client, me_detail_url, user, method, expected_status_code
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(me_detail_url)
            assert response.status_code == expected_status_code
