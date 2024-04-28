import random

import factory

from faker import Faker

from .models import Employee
from authentication.factories import UserFactory


faker = Faker()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    department = factory.LazyAttribute(lambda x: random.randrange(0, 6))
