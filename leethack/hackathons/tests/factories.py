from datetime import timedelta

import factory
from faker import Faker
from django.utils import timezone

from leethack.users.tests.factories import UserFactory

from ..models import Hackathon, Category


faker = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")

    class Meta:
        model = Category


class HackathonFactory(factory.django.DjangoModelFactory):
    host = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.SubFactory(CategoryFactory)
    prize = factory.Faker("pyint", min_value=0, max_value=100000)

    @factory.lazy_attribute
    def start_datetime(self):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        return timezone.make_aware(
            faker.date_time_between(month_start, next_month - timedelta(seconds=1))
        )

    @factory.lazy_attribute
    def end_datetime(self):
        month_end = self.start_datetime.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(seconds=1)
        return timezone.make_aware(
            faker.date_time_between(
                start_date=self.start_datetime + timedelta(minutes=1),
                end_date=month_end,
            )
        )

    @factory.lazy_attribute
    def winner(self):
        from leethack.participations.tests.factories import ParticipantFactory

        if timezone.now() > self.end_datetime:
            return ParticipantFactory()
        return None

    class Meta:
        model = Hackathon
