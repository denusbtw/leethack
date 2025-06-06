import pytest

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from leethack.core.tests.utils import create_test_image

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

    def test_profile_picture_gets_new_unique_name(self, user_factory):
        image = create_test_image()
        uploaded_file = SimpleUploadedFile(
            "image.jpg", image.read(), content_type="image/jpeg"
        )
        user = user_factory(profile_picture=uploaded_file)
        assert len(user.profile_picture.name) > len(uploaded_file.name)

    def test_profile_background_gets_new_unique_name(self, user_factory):
        image = create_test_image(size=(1920, 1080))
        uploaded_file = SimpleUploadedFile(
            "image.jpg", image.read(), content_type="image/jpeg"
        )
        user = user_factory(profile_background=uploaded_file)
        assert len(user.profile_background.name) > len(uploaded_file.name)
