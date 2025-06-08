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

    def test_search_by_username(
        self,
        api_client,
        list_url,
        hackathon,
        participation_request_factory,
        john,
        alice,
        admin_user,
    ):
        api_client.force_authenticate(user=admin_user)
        participation_request_factory(user=john, hackathon=hackathon)
        participation_request_factory(user=alice, hackathon=hackathon)

        response = api_client.get(list_url, {"search": "jo"})
        assert response.status_code == status.HTTP_200_OK
        usernames = {
            participant["user"]["username"] for participant in response.data["results"]
        }
        assert "john" in usernames
        assert all("jo" in username for username in usernames)

    def test_pagination_works(
        self, api_client, list_url, hackathon, participation_request_factory, admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        participation_request_factory.create_batch(5, hackathon=hackathon)
        response = api_client.get(list_url, {"page_size": 2})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert "count" in response.data
        assert response.data["count"] == 5

    def test_cannot_create_request_if_previous_rejected(
        self,
        api_client,
        list_url,
        user,
        participation_request_factory,
        hackathon,
    ):
        api_client.force_authenticate(user=user)
        participation_request_factory(
            user=user, hackathon=hackathon, status=ParticipationRequest.Status.REJECTED
        )

        response = api_client.post(list_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_create_request_if_previous_pending(
        self,
        api_client,
        list_url,
        user,
        participation_request_factory,
        hackathon,
    ):
        api_client.force_authenticate(user=user)
        participation_request_factory(
            user=user, hackathon=hackathon, status=ParticipationRequest.Status.PENDING
        )

        response = api_client.post(list_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_create_request_if_previous_approved(
        self,
        api_client,
        list_url,
        user,
        participation_request_factory,
        hackathon,
    ):
        api_client.force_authenticate(user=user)
        participation_request_factory(
            user=user, hackathon=hackathon, status=ParticipationRequest.Status.APPROVED
        )

        response = api_client.post(list_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


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

    def test_patch_approve_request(
        self, api_client, detail_url, hackathon, participation_request
    ):
        api_client.force_authenticate(user=hackathon.host)
        data = {"status": ParticipationRequest.Status.APPROVED}
        response = api_client.patch(detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK
        participation_request.refresh_from_db()
        assert participation_request.status == data["status"]

    def test_patch_invalid_data(
        self, api_client, detail_url, hackathon, participation_request
    ):
        api_client.force_authenticate(user=hackathon.host)
        data = {"status": "invalid"}
        response = api_client.patch(detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
