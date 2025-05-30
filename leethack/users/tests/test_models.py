import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUser:

    def test_username_is_extracted_from_email(self, user_factory):
        user = user_factory(email="testemail@email.com")
        assert user.username == "testemail"

    def test_is_host_true(self, user_factory):
        user = user_factory(role=User.Role.HOST)
        assert user.is_host

    def test_is_host_false(self, user_factory):
        user = user_factory(role=User.Role.USER)
        assert not user.is_host
