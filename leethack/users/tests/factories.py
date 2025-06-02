import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: f"user_{n}@email.com")
    role = factory.Faker("random_element", elements=User.Role.choices)

    class Meta:
        model = User
