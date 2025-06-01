import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


@pytest.fixture
def my_participated_hackathon_list_url():
    return reverse("api:v1:my_participated_hackathon_list")


@pytest.fixture
def my_hosted_hackathon_list_url():
    return reverse("api:v1:my_hosted_hackathon_list")


@pytest.fixture
def user_hosted_hackathon_list(host):
    return reverse("api:v1:user_hosted_hackathon_list", kwargs={"user_id": host.pk})


@pytest.mark.django_db
class TestMyParticipatedHackathonListAPIView:

    def test_lists_only_hackathons_participated_by_request_user(
        self, api_client, my_participated_hackathon_list_url, user, participant_factory
    ):
        api_client.force_authenticate(user=user)
        participant_factory.create_batch(2, user=user)
        participant_factory.create_batch(3)

        response = api_client.get(my_participated_hackathon_list_url)
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
            my_participated_hackathon_list_url,
            method,
            expected_status_code,
        ):
            response = getattr(api_client, method)(my_participated_hackathon_list_url)
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
            my_participated_hackathon_list_url,
            user,
            method,
            expected_status_code,
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(my_participated_hackathon_list_url)
            assert response.status_code == expected_status_code

    class TestFilter:

        def test_by_category_slug(
            self,
            api_client,
            my_participated_hackathon_list_url,
            category_factory,
            hackathon_factory,
            participant_factory,
            user,
        ):
            web_development = category_factory(title="Web Development")
            ai = category_factory(title="AI")
            web_hackathon = hackathon_factory(category=web_development)
            ai_hackathon = hackathon_factory(category=ai)

            participant_factory(hackathon=web_hackathon, user=user)
            participant_factory(hackathon=ai_hackathon, user=user)

            api_client.force_authenticate(user=user)
            response = api_client.get(
                my_participated_hackathon_list_url, {"category": ai.slug}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(ai_hackathon.id)}

        @pytest.mark.parametrize("param", ["active", "past", "dasjirq"])
        def test_by_hackathon_status(
            self,
            api_client,
            my_participated_hackathon_list_url,
            user,
            hackathon_factory,
            participant_factory,
            past_date,
            future_date,
            param,
        ):
            now = timezone.now()
            active_hackathon = hackathon_factory(
                start_datetime=past_date, end_datetime=future_date
            )
            past_hackathon = hackathon_factory(
                start_datetime=past_date, end_datetime=timezone.now()
            )

            participant_factory(hackathon=active_hackathon, user=user)
            participant_factory(hackathon=past_hackathon, user=user)

            expected_ids = {
                "active": {str(active_hackathon.id)},
                "past": {str(past_hackathon.id)},
            }.get(param, {str(active_hackathon.id), str(past_hackathon.id)})

            api_client.force_authenticate(user=user)
            response = api_client.get(
                my_participated_hackathon_list_url, {"hackathon_status": param}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == expected_ids

        def test_by_start_after(
            self,
            api_client,
            my_participated_hackathon_list_url,
            hackathon_factory,
            participant_factory,
            user,
        ):
            hackathon1 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            participant_factory(hackathon=hackathon1, user=user)
            participant_factory(hackathon=hackathon2, user=user)

            api_client.force_authenticate(user=user)
            query_params = {
                "start_after": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(my_participated_hackathon_list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon2.id)}

        def test_by_end_before(
            self,
            api_client,
            my_participated_hackathon_list_url,
            hackathon_factory,
            participant_factory,
            user,
        ):
            hackathon1 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            participant_factory(hackathon=hackathon1, user=user)
            participant_factory(hackathon=hackathon2, user=user)

            api_client.force_authenticate(user=user)
            query_params = {
                "end_before": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(my_participated_hackathon_list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon1.id)}

        def test_by_winner(
            self,
            api_client,
            my_participated_hackathon_list_url,
            hackathon_factory,
            participant_factory,
            john,
            alice,
            user,
        ):
            john_hackathon = hackathon_factory(winner=participant_factory(user=john))
            alice_hackathon = hackathon_factory(winner=participant_factory(user=alice))

            participant_factory(hackathon=john_hackathon, user=user)
            participant_factory(hackathon=alice_hackathon, user=user)

            api_client.force_authenticate(user=user)
            response = api_client.get(
                my_participated_hackathon_list_url, {"winner": "john"}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {
                str(john_hackathon.id)
            }


@pytest.mark.django_db
class TestMyHostedHackathonListAPIView:

    def test_lists_only_hackathons_hosted_by_request_user(
        self, api_client, my_hosted_hackathon_list_url, host, hackathon_factory
    ):
        api_client.force_authenticate(user=host)

        hackathon_factory.create_batch(2, host=host)
        hackathon_factory.create_batch(3)

        response = api_client.get(my_hosted_hackathon_list_url)
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
            my_hosted_hackathon_list_url,
            method,
            expected_status_code,
        ):
            response = getattr(api_client, method)(my_hosted_hackathon_list_url)
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
            my_hosted_hackathon_list_url,
            user,
            method,
            expected_status_code,
        ):
            api_client.force_authenticate(user=user)
            response = getattr(api_client, method)(my_hosted_hackathon_list_url)
            assert response.status_code == expected_status_code

    class TestFilter:

        def test_by_category_slug(
            self,
            api_client,
            my_hosted_hackathon_list_url,
            category_factory,
            hackathon_factory,
            host,
        ):
            web_development = category_factory(title="Web Development")
            ai = category_factory(title="AI")
            web_hackathon = hackathon_factory(host=host, category=web_development)
            ai_hackathon = hackathon_factory(host=host, category=ai)

            api_client.force_authenticate(user=host)
            response = api_client.get(
                my_hosted_hackathon_list_url, {"category": ai.slug}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(ai_hackathon.id)}

        @pytest.mark.parametrize("param", ["active", "past", "dasjirq"])
        def test_by_hackathon_status(
            self,
            api_client,
            my_hosted_hackathon_list_url,
            host,
            hackathon_factory,
            past_date,
            future_date,
            param,
        ):
            now = timezone.now()
            active_hackathon = hackathon_factory(
                host=host, start_datetime=past_date, end_datetime=future_date
            )
            past_hackathon = hackathon_factory(
                host=host, start_datetime=past_date, end_datetime=timezone.now()
            )

            expected_ids = {
                "active": {str(active_hackathon.id)},
                "past": {str(past_hackathon.id)},
            }.get(param, {str(active_hackathon.id), str(past_hackathon.id)})

            api_client.force_authenticate(user=host)
            response = api_client.get(
                my_hosted_hackathon_list_url, {"hackathon_status": param}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == expected_ids

        def test_by_start_after(
            self,
            api_client,
            my_hosted_hackathon_list_url,
            host,
            hackathon_factory,
            user,
        ):
            hackathon1 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            api_client.force_authenticate(user=host)
            query_params = {
                "start_after": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(my_hosted_hackathon_list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon2.id)}

        def test_by_end_before(
            self,
            api_client,
            my_hosted_hackathon_list_url,
            hackathon_factory,
            host,
        ):
            hackathon1 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            api_client.force_authenticate(user=host)
            query_params = {
                "end_before": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(my_hosted_hackathon_list_url, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon1.id)}

        def test_by_winner(
            self,
            api_client,
            my_hosted_hackathon_list_url,
            hackathon_factory,
            participant_factory,
            john,
            alice,
            host,
        ):
            john_hackathon = hackathon_factory(
                host=host, winner=participant_factory(user=john)
            )
            alice_hackathon = hackathon_factory(
                host=host, winner=participant_factory(user=alice)
            )

            api_client.force_authenticate(user=host)
            response = api_client.get(my_hosted_hackathon_list_url, {"winner": "john"})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {
                str(john_hackathon.id)
            }


@pytest.mark.django_db
class TestUserHostedHackathonListAPIView:

    def test_lists_only_hackathons_hosted_by_specific_user(
        self, api_client, user_hosted_hackathon_list, host, hackathon_factory
    ):
        hackathon_factory.create_batch(2, host=host)
        hackathon_factory.create_batch(3)

        response = api_client.get(user_hosted_hackathon_list)
        assert response.status_code == status.HTTP_200_OK
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
            self,
            api_client,
            user_hosted_hackathon_list,
            method,
            expected_status_code,
        ):
            response = getattr(api_client, method)(user_hosted_hackathon_list)
            assert response.status_code == expected_status_code

    class TestFilter:

        def test_by_category_slug(
            self,
            api_client,
            user_hosted_hackathon_list,
            category_factory,
            hackathon_factory,
            host,
            user,
        ):
            web_development = category_factory(title="Web Development")
            ai = category_factory(title="AI")
            web_hackathon = hackathon_factory(host=host, category=web_development)
            ai_hackathon = hackathon_factory(host=host, category=ai)

            api_client.force_authenticate(user=user)
            response = api_client.get(user_hosted_hackathon_list, {"category": ai.slug})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(ai_hackathon.id)}

        @pytest.mark.parametrize("param", ["active", "past", "dasjirq"])
        def test_by_hackathon_status(
            self,
            api_client,
            user_hosted_hackathon_list,
            host,
            user,
            hackathon_factory,
            past_date,
            future_date,
            param,
        ):
            active_hackathon = hackathon_factory(
                host=host, start_datetime=past_date, end_datetime=future_date
            )
            past_hackathon = hackathon_factory(
                host=host, start_datetime=past_date, end_datetime=timezone.now()
            )

            expected_ids = {
                "active": {str(active_hackathon.id)},
                "past": {str(past_hackathon.id)},
            }.get(param, {str(active_hackathon.id), str(past_hackathon.id)})

            api_client.force_authenticate(user=user)
            response = api_client.get(
                user_hosted_hackathon_list, {"hackathon_status": param}
            )
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == expected_ids

        def test_by_start_after(
            self,
            api_client,
            user_hosted_hackathon_list,
            host,
            hackathon_factory,
            user,
        ):
            hackathon1 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            api_client.force_authenticate(user=user)
            query_params = {
                "start_after": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(user_hosted_hackathon_list, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon2.id)}

        def test_by_end_before(
            self,
            api_client,
            user_hosted_hackathon_list,
            hackathon_factory,
            host,
            user,
        ):
            hackathon1 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 1, 1)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 1, 9)),
            )
            hackathon2 = hackathon_factory(
                host=host,
                start_datetime=timezone.make_aware(datetime.datetime(2025, 3, 2)),
                end_datetime=timezone.make_aware(datetime.datetime(2025, 3, 13)),
            )

            api_client.force_authenticate(user=user)
            query_params = {
                "end_before": timezone.make_aware(datetime.datetime(2025, 2, 8))
            }
            response = api_client.get(user_hosted_hackathon_list, query_params)
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {str(hackathon1.id)}

        def test_by_winner(
            self,
            api_client,
            user_hosted_hackathon_list,
            hackathon_factory,
            participant_factory,
            john,
            alice,
            host,
            user,
        ):
            john_hackathon = hackathon_factory(
                host=host, winner=participant_factory(user=john)
            )
            alice_hackathon = hackathon_factory(
                host=host, winner=participant_factory(user=alice)
            )

            api_client.force_authenticate(user=user)
            response = api_client.get(user_hosted_hackathon_list, {"winner": "john"})
            assert response.status_code == status.HTTP_200_OK
            assert {h["id"] for h in response.data["results"]} == {
                str(john_hackathon.id)
            }
