import datetime
from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from leethack.hackathons.tests.factories import CategoryFactory, HackathonFactory
from leethack.participations.models import ParticipationRequest
from leethack.participations.tests.factories import (
    ParticipantFactory,
    ParticipationRequestFactory,
)
from leethack.users.tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def past_date():
    return timezone.now() - datetime.timedelta(days=7)


@pytest.fixture
def future_date():
    return timezone.now() + datetime.timedelta(days=7)


@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def user(user_factory):
    return user_factory(role=User.Role.USER)


@pytest.fixture
def host(user_factory):
    return user_factory(role=User.Role.HOST)


@pytest.fixture
def category_factory():
    return CategoryFactory


@pytest.fixture
def hackathon_factory():
    return HackathonFactory


@pytest.fixture
def participant_factory():
    return ParticipantFactory


@pytest.fixture
def participation_request_factory():
    return ParticipationRequestFactory


@pytest.fixture
def hackathon(hackathon_factory):
    return hackathon_factory()


@pytest.fixture
def participation_request(hackathon, participation_request_factory):
    return participation_request_factory(hackathon=hackathon)


@pytest.fixture
def approved_participation_request(hackathon, participation_request_factory):
    return participation_request_factory(
        status=ParticipationRequest.Status.APPROVED, hackathon=hackathon
    )


@pytest.fixture
def pending_participation_request(hackathon, participation_request_factory):
    return participation_request_factory(
        status=ParticipationRequest.Status.PENDING, hackathon=hackathon
    )


@pytest.fixture
def rejected_participation_request(hackathon, participation_request_factory):
    return participation_request_factory(
        status=ParticipationRequest.Status.REJECTED, hackathon=hackathon
    )


@pytest.fixture
def john(user_factory):
    return user_factory(username="john", email="john@email.com")


@pytest.fixture
def alice(user_factory):
    return user_factory(username="alice", email="alice@email.com")


@pytest.fixture
def image_file():
    buffer = BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return SimpleUploadedFile(
        name="test.jpg",
        content=buffer.read(),
        content_type="image/jpeg",
    )


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath
