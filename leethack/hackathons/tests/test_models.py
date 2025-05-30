import datetime

import pytest
from django.db import IntegrityError
from django.utils import timezone


@pytest.mark.django_db
class TestHackathonModel:

    def test_error_if_start_datetime_after_end_datetime(
        self, hackathon_factory, past_date, future_date
    ):
        with pytest.raises(IntegrityError):
            hackathon_factory(start_datetime=future_date, end_datetime=past_date)

    def test_is_active_true(self, hackathon_factory, past_date, future_date):
        hackathon = hackathon_factory(
            start_datetime=past_date, end_datetime=future_date
        )
        assert hackathon.is_active

    def test_is_active_false(self, hackathon_factory):
        start_datetime = timezone.make_aware(datetime.datetime(2000, 1, 1))
        end_datetime = timezone.make_aware(datetime.datetime(2000, 1, 8))
        hackathon = hackathon_factory(
            start_datetime=start_datetime, end_datetime=end_datetime
        )
        assert not hackathon.is_active
