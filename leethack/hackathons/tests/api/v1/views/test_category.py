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
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_405_METHOD_NOT_ALLOWED),
            ],
        )
        def test_anonymous_user(
            self, api_client, list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

    def test_search(self, api_client, list_url, category_factory):
        category_factory(title="Python")
        category_factory(title="Django")
        category_factory(title="Flask")

        response = api_client.get(list_url, {"search": "Djan"})
        titles = {item["title"] for item in response.data["results"]}
        assert response.status_code == status.HTTP_200_OK
        assert "Django" in titles
        assert all("Djan" in title for title in titles)

    def test_ordering_asc(self, api_client, list_url, category_factory):
        category_factory(title="B category")
        category_factory(title="A category")

        response = api_client.get(list_url, {"ordering": "title"})
        titles = [item["title"] for item in response.data["results"]]
        assert response.status_code == status.HTTP_200_OK
        assert titles == sorted(titles)

    def test_ordering_desc(self, api_client, list_url, category_factory):
        category_factory(title="A Category")
        category_factory(title="B Category")

        response = api_client.get(list_url, {"ordering": "-title"})
        titles = [item["title"] for item in response.data["results"]]
        assert response.status_code == status.HTTP_200_OK
        assert titles == sorted(titles, reverse=True)

    def test_pagination(self, api_client, list_url, category_factory):
        category_factory.create_batch(5)
        response = api_client.get(list_url, {"page_size": 3})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3
        assert "count" in response.data
        assert response.data["count"] == 5

    def test_non_existent_page(self, api_client, list_url, category_factory):
        category_factory.create_batch(3)
        response = api_client.get(list_url, {"page": 100})
        assert response.status_code == status.HTTP_404_NOT_FOUND
