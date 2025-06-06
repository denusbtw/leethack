from datetime import timedelta

import factory
from faker import Faker
from django.utils import timezone
from django.contrib.auth import get_user_model

from leethack.users.tests.factories import UserFactory

from ..models import Hackathon, Category
from ...participations.models import Participant

User = get_user_model()
fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"category_{n}")

    class Meta:
        model = Category


class HackathonFactory(factory.django.DjangoModelFactory):
    host = factory.SubFactory(UserFactory, role=User.Role.HOST)
    title = factory.Sequence(lambda n: f"hackathon_{n}")
    description = factory.Faker("paragraph", nb_sentences=3)
    category = factory.SubFactory(CategoryFactory)
    prize = factory.Faker("pyint", min_value=0, max_value=100000)

    @factory.lazy_attribute
    def start_datetime(self):
        return timezone.make_aware(
            fake.date_time_between(
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=60),
            )
        )

    @factory.lazy_attribute
    def end_datetime(self):
        return timezone.make_aware(
            fake.date_time_between(
                start_date=self.start_datetime + timedelta(days=1),
                end_date=self.start_datetime + timedelta(days=30),
            )
        )

    @factory.post_generation
    def winner(self, create: bool, extracted: Participant, *args, **kwargs):
        if not create:
            return

        from leethack.participations.tests.factories import ParticipantFactory

        if extracted:
            self.winner = extracted
            self.save()
            return

        if timezone.now() > self.end_datetime:
            self.winner = ParticipantFactory(hackathon=self)
            self.save()

    class Meta:
        model = Hackathon
        skip_postgeneration_save = True
