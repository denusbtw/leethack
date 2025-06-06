import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from leethack.core.tests.utils import create_test_image
from leethack.hackathons.api.v1.serializers import (
    HackathonUpdateSerializer,
    HackathonCreateSerializer,
)


@pytest.fixture
def valid_file():
    size = (
        settings.HACKATHON_IMAGE_CONFIG["min_width"],
        settings.HACKATHON_IMAGE_CONFIG["min_height"],
    )
    valid_image = create_test_image(size=size)
    uploaded_file = SimpleUploadedFile(
        "valid.jpg", valid_image.read(), content_type="image/jpeg"
    )
    valid_image.seek(0)
    return uploaded_file


@pytest.fixture
def invalid_file():
    return SimpleUploadedFile(
        "invalid.jpg", b"not-an-image-content", content_type="image/jpeg"
    )


@pytest.fixture
def data(host, past_date, future_date):
    return {
        "host": host.pk,
        "title": "test hackathon title",
        "description": "test hackathon description",
        "prize": 1000,
        "start_datetime": past_date,
        "end_datetime": future_date,
        "image": None,
    }


@pytest.mark.django_db
class TestHackathonUpdateSerializer:

    def test_error_if_trying_to_set_winner_on_active_hackathon(
        self, participant_factory, hackathon_factory, future_date, past_date
    ):
        hackathon = hackathon_factory(
            start_datetime=past_date, end_datetime=future_date
        )
        participant = participant_factory(hackathon=hackathon)

        data = {"winner": participant.pk}
        serializer = HackathonUpdateSerializer(hackathon, data=data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_error_if_trying_to_set_winner_not_participant_of_hackathon(
        self, participant_factory, hackathon_factory, past_date, future_date
    ):
        hackathon = hackathon_factory(
            start_datetime=past_date, end_datetime=future_date
        )

        winner = participant_factory()
        data = {"winner": winner.pk}

        serializer = HackathonUpdateSerializer(hackathon, data)
        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    class TestImage:

        def test_valid_image_pass(self, hackathon, valid_file):
            data = {"image": valid_file}
            serializer = HackathonUpdateSerializer(hackathon, data=data)
            assert serializer.is_valid(), serializer.errors

        def test_invalid_image_raises_validation_error(self, hackathon, invalid_file):
            data = {"image": invalid_file}
            serializer = HackathonUpdateSerializer(hackathon, data=data)
            with pytest.raises(ValidationError):
                serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestHackathonCreateSerializer:

    class TestImage:

        def test_valid_image_pass(self, valid_file, data):
            data["image"] = valid_file
            serializer = HackathonCreateSerializer(data=data)
            assert serializer.is_valid(), serializer.errors

        def test_invalid_image_raises_validation_error(self, invalid_file, data):
            data["image"] = invalid_file
            serializer = HackathonCreateSerializer(data=data)
            with pytest.raises(ValidationError):
                serializer.is_valid(raise_exception=True)
