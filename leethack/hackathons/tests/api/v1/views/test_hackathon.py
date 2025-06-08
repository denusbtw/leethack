import datetime

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from leethack.core.tests.utils import create_test_image
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
    image_file = SimpleUploadedFile(
        "test.jpg", create_test_image(fmt="JPEG").read(), content_type="image/jpeg"
    )
    return {
        "title": "test hackathon",
        "description": "test decsription",
        "category": category.pk,
        "prize": 1000,
        "start_datetime": past_date,
        "end_datetime": future_date,
        "image": image_file,
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
        def test_not_host(
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

    class TestFilter:

        def test_by_category_slug(
            self, api_client, list_url, category_factory, hackathon_factory
        ):
            web_development = category_factory(title="Web Development")
            ai = category_factory(title="AI")
            web_hackathon = hackathon_factory(category=web_development)
            ai_hackathon = hackathon_factory(category=ai)

            response = api_client.get(list_url, {"category": ai.slug})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(ai_hackathon.id)}

        @pytest.mark.parametrize("param", ["active", "past", "dasjirq"])
        def test_by_hackathon_status(
            self, api_client, list_url, hackathon_factory, past_date, future_date, param
        ):
            now = timezone.now()
            active_hackathon = hackathon_factory(
                start_datetime=past_date, end_datetime=future_date
            )
            past_hackathon = hackathon_factory(
                start_datetime=past_date, end_datetime=timezone.now()
            )

            expected_ids = {
                "active": {str(active_hackathon.id)},
                "past": {str(past_hackathon.id)},
            }.get(param, {str(active_hackathon.id), str(past_hackathon.id)})

            response = api_client.get(list_url, {"hackathon_status": param})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == expected_ids

        def test_by_start_after(self, api_client, list_url, hackathon_factory):
            hackathon1 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            query_params = {
                "start_after": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon2.id)}

        def test_by_end_before(self, api_client, list_url, hackathon_factory):
            hackathon1 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            query_params = {
                "end_before": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon1.id)}

        def test_by_winner(
            self,
            api_client,
            list_url,
            hackathon_factory,
            participant_factory,
            john,
            alice,
        ):
            john_hackathon = hackathon_factory(winner=participant_factory(user=john))
            alice_hackathon = hackathon_factory(winner=participant_factory(user=alice))

            response = api_client.get(list_url, {"winner": "john"})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {
                str(john_hackathon.id)
            }

    def test_create_invalid_data_returns_400(
        self, api_client, list_url, host, past_date, future_date
    ):
        api_client.force_authenticate(user=host)
        invalid_data = {
            "title": "",
            "start_datetime": future_date,
            "past_date": past_date,
        }
        response = api_client.post(list_url, data=invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "end_datetime" in response.data

    def test_create_ignores_host_field_in_request(
        self, api_client, list_url, data, user, host
    ):
        api_client.force_authenticate(user=host)

        data["host"] = user.pk
        response = api_client.post(list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        hackathon_id = response.data["id"]
        hackathon = Hackathon.objects.get(pk=hackathon_id)
        assert hackathon.host == host

    def test_pagination_works(self, api_client, list_url, hackathon_factory):
        hackathon_factory.create_batch(5)
        response = api_client.get(list_url, {"page_size": 2})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert "count" in response.data
        assert response.data["count"] == 5

    def test_ordering_by_prize_asc(self, api_client, list_url, hackathon_factory):
        hackathon_factory(prize="500")
        hackathon_factory(prize="1000")
        hackathon_factory(prize="750")

        response = api_client.get(list_url, {"ordering": "prize"})
        assert response.status_code == status.HTTP_200_OK
        prizes = [hackathon["prize"] for hackathon in response.data["results"]]
        assert prizes == sorted(prizes)

    def test_ordering_by_prize_desc(self, api_client, list_url, hackathon_factory):
        hackathon_factory(prize="500")
        hackathon_factory(prize="1000")
        hackathon_factory(prize="750")

        response = api_client.get(list_url, {"ordering": "-prize"})
        assert response.status_code == status.HTTP_200_OK
        prizes = [hackathon["prize"] for hackathon in response.data["results"]]
        assert prizes == sorted(prizes, reverse=True)


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

    def test_patch_valid_data(self, api_client, detail_url, hackathon):
        api_client.force_authenticate(user=hackathon.host)
        response = api_client.patch(detail_url, data={"title": "updated title"})
        assert response.status_code == status.HTTP_200_OK
        hackathon.refresh_from_db()
        assert hackathon.title == "updated title"

    def test_patch_invalid_data(self, api_client, detail_url, hackathon):
        api_client.force_authenticate(user=hackathon.host)
        response = api_client.patch(detail_url, data={"prize": "invalid"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_host_field_cannot_be_modified(
        self, api_client, detail_url, hackathon, user
    ):
        api_client.force_authenticate(user=hackathon.host)
        old_host = hackathon.host
        response = api_client.patch(detail_url, data={"host": user.pk})
        assert response.status_code == status.HTTP_200_OK
        hackathon.refresh_from_db()
        assert hackathon.host == old_host
