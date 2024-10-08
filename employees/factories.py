import random

import factory

from faker import Faker

from .models import Employee
from authentication.factories import UserFactory


faker = Faker()


def generate_random_color():
    return f'#{random.randint(0, 0xFFFFFF)}'


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    department = factory.LazyAttribute(lambda x: random.randrange(0, 6))
    phone_number = factory.LazyAttribute(lambda x: random.randrange(10**8, 10**9))
    color = factory.LazyFunction(generate_random_color)
