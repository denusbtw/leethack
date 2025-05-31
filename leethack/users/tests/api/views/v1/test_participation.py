import pytest
from django.urls import reverse
from rest_framework import status

from leethack.conftest import participation_request
from leethack.participations.models import ParticipationRequest


@pytest.fixture
def my_participation_request_list_url():
    return reverse("api:v1:my_participation_request_list")


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
            self,
            api_client,
            my_participation_request_list_url,
            method,
            expected_status_code,
        ):
            response = getattr(api_client, method)(my_participation_request_list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_405_METHOD_NOT_ALLOWED),
            ],
        )
        def test_authenticated_user(
            self,
            api_client,
            my_participation_request_list_url,
            user,
            method,
            expected_status_code,
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(my_participation_request_list_url)
            assert response.status_code == expected_status_code


@pytest.mark.django_db
class TestMyParticipationRequestDetailAPIView:

    @pytest.mark.parametrize(
        "request_status, expected_status_code",
        [
            (ParticipationRequest.Status.APPROVED, status.HTTP_403_FORBIDDEN),
            (ParticipationRequest.Status.PENDING, status.HTTP_204_NO_CONTENT),
            (ParticipationRequest.Status.REJECTED, status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_user_can_delete_only_pending_request(
        self,
        api_client,
        my_participation_request_detail_url,
        participation_request,
        request_status,
        expected_status_code,
    ):
        participation_request.status = request_status
        participation_request.save()

        api_client.force_authenticate(participation_request.user)
        response = api_client.delete(my_participation_request_detail_url)
        assert response.status_code == expected_status_code

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
            self,
            api_client,
            my_participation_request_detail_url,
            method,
            expected_status_code,
        ):
            response = getattr(api_client, method)(my_participation_request_detail_url)
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
        def test_authenticated_user(
            self,
            api_client,
            participation_request,
            my_participation_request_detail_url,
            method,
            expected_status_code,
        ):
            participation_request.status = ParticipationRequest.Status.PENDING
            participation_request.save()

            api_client.force_authenticate(user=participation_request.user)
            response = getattr(api_client, method)(my_participation_request_detail_url)
            assert response.status_code == expected_status_code


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
            self, api_client, my_participation_list_url, method, expected_status_code
        ):
            response = getattr(api_client, method)(my_participation_list_url)
            assert response.status_code == expected_status_code

        @pytest.mark.parametrize(
            "method, expected_status_code",
            [
                ("get", status.HTTP_200_OK),
                ("post", status.HTTP_405_METHOD_NOT_ALLOWED),
            ],
        )
        def test_authenticated_user(
            self,
            api_client,
            my_participation_list_url,
            user,
            method,
            expected_status_code,
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(my_participation_list_url)
            assert response.status_code == expected_status_code
