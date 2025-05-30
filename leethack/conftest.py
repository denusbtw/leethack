import datetime

import pytest
from django.utils import timezone

from rest_framework.test import APIClient

from leethack.hackathons.tests.factories import CategoryFactory, HackathonFactory
from leethack.participations.tests.factories import (
    ParticipantFactory,
    ParticipationRequestFactory,
)
from leethack.users.tests.factories import UserFactory


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
