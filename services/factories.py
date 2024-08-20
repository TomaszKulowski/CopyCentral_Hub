import random

import factory

from faker import Faker

from .models import Brand, Model, Service


BRANDS = [
    'Konica Minolta',
    'HP',
    'Canon',
    'Epson',
    'Brother',
    'Lexmark',
    'Xerox',
    'Samsung',
    'Dell',
    'Kyocera',
    'Sharp',
]

MODELS = [
    'LaserJet Pro M404n',
    'OfficeJet Pro 9015',
    'Color LaserJet Pro MFP M281fdw',
    'ENVY Photo 7155',
    'PIXMA MX922',
    'imageCLASS MF634Cdw',
    'PIXMA Pro-100',
    'BIZHUB C224',
    'BIZHUB C308',
    'BIZHUB C360i',
]

faker = Faker()


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda x: f'{random.choice(BRANDS)}-{random.randint(1, 10**5)}')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        while True:
            name = f'{random.choice(BRANDS)}-{random.randint(1, 10**5)}'
            if not Brand.objects.filter(name=name).exists():
                return super()._create(model_class, *args, **kwargs)


class ModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Model

    name = factory.LazyAttribute(lambda x: f'{random.choice(MODELS)}-{random.randint(1, 10**5)}')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        while True:
            name = f'{random.choice(MODELS)}-{random.randint(1, 10**5)}'
            if not Model.objects.filter(name=name).exists():
                return super()._create(model_class, *args, **kwargs)


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    device_brand = factory.Maybe(factory.SubFactory(BrandFactory))
    device_model = factory.Maybe(factory.SubFactory(ModelFactory))
    name = factory.LazyAttribute(lambda x: faker.sentence(3))
    price_net = factory.LazyAttribute(lambda x: round(random.uniform(500.1, 6000.0), 2))
    description = factory.LazyAttribute(lambda x: faker.sentence(20))
