import pytest
from django.urls import reverse
from rest_framework import status

from leethack.conftest import hackathon


@pytest.fixture
def list_url(hackathon):
    return reverse(
        "api:v1:hackathon_participant_list", kwargs={"hackathon_id": hackathon.pk}
    )


@pytest.fixture
def participant(hackathon, participant_factory):
    print(hackathon.start_datetime, hackathon.end_datetime)
    return participant_factory(hackathon=hackathon)


@pytest.fixture
def detail_url(participant):
    return reverse(
        "api:v1:hackathon_participant_detail",
        kwargs={"hackathon_id": participant.hackathon_id, "pk": participant.pk},
    )


@pytest.mark.django_db
class TestHackathonParticipantListAPIView:

    def test_lists_only_participants_of_specific_hackathon(
        self, api_client, list_url, admin_user, hackathon, participant_factory
    ):
        participant_factory.create_batch(2, hackathon=hackathon)
        participant_factory.create_batch(3)

        api_client.force_authenticate(user=admin_user)
        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    class TestPermissions:

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_403_FORBIDDEN),
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
                ("get", status.HTTP_403_FORBIDDEN),
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
                ("get", status.HTTP_403_FORBIDDEN),
                ("post", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_host_but_not_hackathon_host(
            self, api_client, list_url, host, method, expected_status_code
        ):
            api_client.force_authenticate(user=host)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_405_METHOD_NOT_ALLOWED),
            ],
        )
        def test_hackathon_host(
            self, api_client, list_url, hackathon, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.host)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_405_METHOD_NOT_ALLOWED),
            ],
        )
        def test_admin_user(
            self, api_client, list_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

    def test_search(
        self,
        api_client,
        list_url,
        hackathon,
        participant_factory,
        user_factory,
        john,
        alice,
        admin_user,
    ):
        api_client.force_authenticate(user=admin_user)

        participant_factory(user=john, hackathon=hackathon)
        participant_factory(user=alice, hackathon=hackathon)

        response = api_client.get(list_url, {"search": "jo"})
        assert response.status_code == status.HTTP_200_OK

        usernames = [
            participant["user"]["username"] for participant in response.data["results"]
        ]
        assert "john" in usernames
        assert all("jo" in username for username in usernames)

    def test_pagination_works(
        self, api_client, list_url, hackathon, participant_factory, admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        participant_factory.create_batch(5, hackathon=hackathon)
        response = api_client.get(list_url, {"page_size": 2})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert "count" in response.data
        assert response.data["count"] == 5


@pytest.mark.django_db
class TestHackathonParticipantDetailAPIView:

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
            self, api_client, detail_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_403_FORBIDDEN),
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
                ("get", status.HTTP_403_FORBIDDEN),
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_host_but_not_hackathon_host(
            self, api_client, detail_url, host, method, expected_status_code
        ):
            api_client.force_authenticate(user=host)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("put", status.HTTP_405_METHOD_NOT_ALLOWED),
                ("patch", status.HTTP_405_METHOD_NOT_ALLOWED),
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
                ("put", status.HTTP_403_FORBIDDEN),
                ("patch", status.HTTP_403_FORBIDDEN),
                ("delete", status.HTTP_403_FORBIDDEN),
            ],
        )
        def test_admin_user(
            self, api_client, detail_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(detail_url)
            assert response.status_code == expected_status_code
