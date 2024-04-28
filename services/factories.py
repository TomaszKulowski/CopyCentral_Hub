import random

import factory

from faker import Faker

from .models import Brand, Model, Service


faker = Faker()


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'Brand-{n}')


class ModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Model

    name = factory.Sequence(lambda n: f'Model-{n}')


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.LazyAttribute(lambda x: faker.sentence(3))
    price_net = factory.LazyAttribute(lambda x: round(random.uniform(500.1, 6000.0), 2))
    description = factory.LazyAttribute(lambda x: faker.sentence(20))
    device_brand = factory.Maybe(factory.SubFactory(BrandFactory))
    device_model = factory.Maybe(factory.SubFactory(ModelFactory))
    device_brand = factory.SubFactory(BrandFactory, name=factory.Sequence(lambda n: f'Device Brand-{n}'))
    device_model = factory.SubFactory(ModelFactory, name=factory.Sequence(lambda n: f'Device Model-{n}'))
