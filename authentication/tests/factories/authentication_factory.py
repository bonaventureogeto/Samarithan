import factory
from faker import Faker

from authentication.models import User

fake = Faker()
role = 'GA'


class UserFactory(factory.DjangoModelFactory):
    """ this class creates test users """
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda _: fake.name())
    last_name = factory.LazyAttribute(lambda _: fake.name())
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.LazyAttribute(lambda _: fake.email())
    role = role
