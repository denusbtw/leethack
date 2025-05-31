import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def list_url():
    return reverse("api:v1:category_list")


@pytest.mark.django_db
class TestCategoryListAPIView:

    def test_returns_all_categories(self, api_client, list_url, category_factory):
        category_factory.create_batch(2)
        response = api_client.get(list_url)
        assert response.data["count"] == 2

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [("get", status.HTTP_200_OK), ("post", status.HTTP_405_METHOD_NOT_ALLOWED)],
        )
        def test_anonymous_user(
            self, api_client, list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code
