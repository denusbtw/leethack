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


@pytest.fixture
def detail_url(participation_request):
    return reverse(
        "api:v1:hackathon_participation_request_detail",
        kwargs={
            "hackathon_id": participation_request.hackathon_id,
            "pk": participation_request.pk,
        },
    )


@pytest.fixture
def data():
    return {"status": ParticipationRequest.Status.APPROVED}


@pytest.mark.django_db
class TestHackathonParticipationRequestListCreateAPIView:

    def test_lists_participation_requests_only_of_specific_hackathon(
        self, api_client, list_url, admin_user, hackathon, participation_request_factory
    ):
        participation_request_factory.create_batch(2, hackathon=hackathon)
        participation_request_factory.create_batch(3)

        api_client.force_authenticate(user=admin_user)
        response = api_client.get(list_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_perform_create_pending_request_and_sets_user_and_hackathon(
        self, api_client, list_url, hackathon, user
    ):
        api_client.force_authenticate(user=user)
        response = api_client.post(list_url)
        assert response.status_code == status.HTTP_201_CREATED

        participation_request = ParticipationRequest.objects.get(pk=response.data["id"])
        assert participation_request.user == user
        assert participation_request.hackathon == hackathon
        assert participation_request.status == ParticipationRequest.Status.PENDING

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
                ("post", status.HTTP_201_CREATED),
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
                ("post", status.HTTP_201_CREATED),
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
                ("post", status.HTTP_201_CREATED),
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
                ("post", status.HTTP_201_CREATED),
            ],
        )
        def test_admin_user(
            self, api_client, list_url, admin_user, method, expected_status_code
        ):
            api_client.force_authenticate(user=admin_user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_403_FORBIDDEN),
                ("post", status.HTTP_400_BAD_REQUEST),
            ],
        )
        def test_hackathon_participant(
            self,
            api_client,
            list_url,
            hackathon,
            participant_factory,
            method,
            expected_status_code,
        ):
            participant = participant_factory(hackathon=hackathon)

            api_client.force_authenticate(user=participant.user)
            response = getattr(api_client, method)(list_url)
            assert response.status_code == expected_status_code

    class TestFilter:

        def test_by_status(
            self,
            api_client,
            list_url,
            admin_user,
            approved_participation_request,
            pending_participation_request,
            rejected_participation_request,
        ):
            api_client.force_authenticate(user=admin_user)
            query_params = {"status": ParticipationRequest.Status.APPROVED}
            response = api_client.get(list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {
                str(approved_participation_request.id)
            }


@pytest.mark.django_db
class TestHackathonParticipationRequestDetailAPIView:

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
                ("put", status.HTTP_200_OK),
                ("patch", status.HTTP_200_OK),
                ("delete", status.HTTP_204_NO_CONTENT),
            ],
        )
        def test_hackathon_host(
            self, api_client, detail_url, hackathon, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.host)
            response = getattr(api_client, method)(detail_url, data=data)
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
            self, api_client, detail_url, hackathon, data, method, expected_status_code
        ):
            api_client.force_authenticate(user=hackathon.host)
            response = getattr(api_client, method)(detail_url, data=data)
            assert response.status_code == expected_status_code
