import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import post_generation


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.LazyFunction(lambda: make_password('password'))
    email = ''

    @post_generation
    def post(self, create, *args, **kwargs):
        self.email = self.username
