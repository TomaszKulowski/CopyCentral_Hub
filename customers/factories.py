import random

import factory

from faker import Faker

from .models import Customer, AdditionalAddress
from authentication.factories import UserFactory


faker = Faker()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda x: faker.company())
    tax = factory.LazyAttribute(lambda x: random.randrange(10**9, 10**10-1))
    billing_country = factory.LazyAttribute(lambda x: faker.country()[:24])
    billing_city = factory.LazyAttribute(lambda x: faker.city())
    billing_postal_code = factory.LazyAttribute(lambda x: faker.postcode())
    billing_street = factory.LazyAttribute(lambda x: faker.street_name()[:24])
    billing_number = factory.LazyAttribute(lambda x: faker.building_number())
    country_calling_code = factory.LazyAttribute(lambda x: faker.country_calling_code()[:8])
    phone_number = factory.LazyAttribute(lambda x: random.randrange(10**8, 10**9))
    email = factory.LazyAttribute(lambda x: faker.email())
    description = factory.LazyAttribute(lambda x: faker.sentence(15))
    payment = factory.LazyAttribute(lambda x: random.randrange(0, 2))


class AdditionalAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdditionalAddress

    customer = factory.SubFactory(CustomerFactory)
    country = factory.LazyAttribute(lambda x: faker.country()[:24])
    city = factory.LazyAttribute(lambda x: faker.city())
    postal_code = factory.LazyAttribute(lambda x: faker.postcode()[:8])
    street = factory.LazyAttribute(lambda x: faker.street_name()[:24])
    number = factory.LazyAttribute(lambda x: faker.building_number())
    description = factory.LazyAttribute(lambda x: faker.sentence(20))
    is_active = True
