import factory

from leethack.hackathons.tests.factories import HackathonFactory
from leethack.users.tests.factories import UserFactory

from ..models import Participant, ParticipationRequest


class ParticipantFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    hackathon = factory.SubFactory(HackathonFactory)

    class Meta:
        model = Participant


class ParticipationRequestFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    hackathon = factory.SubFactory(HackathonFactory)
    status = factory.Faker(
        "random_element", elements=[c[0] for c in ParticipationRequest.Status.choices]
    )

    class Meta:
        model = ParticipationRequest
