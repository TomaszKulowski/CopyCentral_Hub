import random
import string

import factory

from factory import post_generation
from faker import Faker

from .models import Device, Status


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

CHARS = string.ascii_letters + string.digits

faker = Faker()


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    brand = factory.LazyAttribute(lambda x: random.choice(BRANDS))
    model = factory.LazyAttribute(lambda x: random.choice(MODELS))
    serial_number = factory.Sequence(lambda x: f'{faker.unique.uuid4()}_{x}')
    type = factory.LazyAttribute(lambda x: random.randrange(0, 2))
    format = factory.LazyAttribute(lambda x: random.randrange(0, 2))
    total_counter = factory.LazyAttribute(lambda x: random.randrange(0, 10**6))
    mono_counter = None
    color_counter = None
    description = factory.LazyAttribute(lambda x: faker.sentence(10))
    status = factory.LazyAttribute(lambda x: random.choices(Status.choices)[0][0])
    price_net = factory.LazyAttribute(lambda x: round(random.uniform(500.1, 6000.0), 2))

    @post_generation
    def post(self, create, *args, **kwargs):
        if self.type == 0:
            self.mono_counter = self.total_counter
        else:
            self.mono_counter = self.total_counter - random.randint(0, self.total_counter)
            self.color_counter = self.total_counter - self.mono_counter
