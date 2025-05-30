import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    role = factory.Faker("random_element", elements=User.Role.choices)

    class Meta:
        model = User
