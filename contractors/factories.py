import random

import factory

from faker import Faker

from .models import Contractor
from authentication.factories import UserFactory


faker = Faker()


class ContractorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contractor

    user = factory.SubFactory(UserFactory)
    company = factory.LazyAttribute(lambda x: faker.company())
    tax = factory.LazyAttribute(lambda x: random.randrange(10**9, 10**10-1))
    country = factory.LazyAttribute(lambda x: faker.country())
    city = factory.LazyAttribute(lambda x: faker.city())
    postal_code = factory.LazyAttribute(lambda x: faker.postcode())
    street = factory.LazyAttribute(lambda x: faker.street_name())
    number = factory.LazyAttribute(lambda x: faker.building_number())
    country_calling_code = factory.LazyAttribute(lambda x: faker.country_calling_code())
    telephone = factory.LazyAttribute(lambda x: random.randrange(10**8, 10**9))
    description = factory.LazyAttribute(lambda x: faker.sentence(20))
    transfer_payment = factory.LazyAttribute(lambda x: random.randrange(0, 2))
