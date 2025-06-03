import pytest
from django.contrib.auth.password_validation import validate_password


@pytest.mark.django_db
class TestUserFactory:

    def test_generates_valid_password(self, user_factory):
        user = user_factory()
        validate_password(user._raw_password)
        assert user.check_password(user._raw_password)
