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
        return faker.date_time_between(
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=60),
            tzinfo=timezone.get_current_timezone(),
        )

    @factory.lazy_attribute
    def end_datetime(self):
        return faker.date_time_between(
            start_date=self.start_datetime + timedelta(minutes=1),
            end_date=self.start_datetime + timedelta(days=30),
            tzinfo=timezone.get_current_timezone(),
        )

    @factory.lazy_attribute
    def winner(self):
        from leethack.participations.tests.factories import ParticipantFactory

        if timezone.now() > self.end_datetime:
            return ParticipantFactory()
        return None

    class Meta:
        model = Hackathon
