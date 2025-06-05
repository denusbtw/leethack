import pytest
from faker import Faker
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from leethack.core.tests.utils import create_test_image
from django.conf import settings

from leethack.users.api.v1.serializers.user import MeUpdateSerializer

faker = Faker()


@pytest.fixture
def invalid_password():
    return "invalid"


@pytest.fixture
def valid_password():
    return faker.password(
        length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
    )


@pytest.mark.django_db
class TestMeUpdateSerializer:

    class TestPassword:

        def test_error_if_invalid_password(self, user, invalid_password):
            data = {"password": invalid_password}
            serializer = MeUpdateSerializer(user, data=data)
            with pytest.raises(ValidationError):
                serializer.is_valid(raise_exception=True)

        def test_empty(self, user):
            user.set_password("123123qq")
            user.save()

            serializer = MeUpdateSerializer(user, data={})
            assert serializer.is_valid(), serializer.errors
            serializer.save()

            user.refresh_from_db()
            assert user.check_password("123123qq")

        def test_no_error_if_valid_password(self, user, valid_password):
            data = {"password": valid_password}
            serializer = MeUpdateSerializer(user, data=data)
            assert serializer.is_valid(), serializer.errors

    def test_valid_profile_picture_pass(self, user):
        size = (
            settings.PROFILE_PICTURE_CONFIG["min_width"],
            settings.PROFILE_PICTURE_CONFIG["min_height"],
        )
        valid_image = create_test_image(size=size)
        uploaded_file = SimpleUploadedFile(
            "valid.jpg", valid_image.read(), content_type="image/jpeg"
        )
        valid_image.seek(0)

        data = {"profile_picture": uploaded_file}
        serializer = MeUpdateSerializer(user, data=data)
        assert serializer.is_valid(), serializer.errors

    def test_valid_profile_background_pass(self, user):
        size = (
            settings.PROFILE_BACKGROUND_CONFIG["min_width"],
            settings.PROFILE_BACKGROUND_CONFIG["min_height"],
        )
        valid_image = create_test_image(size=size)
        uploaded_file = SimpleUploadedFile(
            "valid.jpg", valid_image.read(), content_type="image/jpeg"
        )
        valid_image.seek(0)

        data = {"profile_background": uploaded_file}
        serializer = MeUpdateSerializer(user, data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_image_raises_validation_error(self, user):
        invalid_file = SimpleUploadedFile(
            "invalid.jpg", b"not-an-image-content", content_type="image/jpeg"
        )

        data = {
            "profile_picture": invalid_file,
            "profile_background": invalid_file,
        }

        serializer = MeUpdateSerializer(user, data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
