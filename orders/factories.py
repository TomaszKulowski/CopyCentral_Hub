import random

from datetime import timedelta
from unittest.mock import patch

import factory

from factory import post_generation
from faker import Faker

from .models import OrderService, Region, ShortDescription, Order
from customers.factories import CustomerFactory, AdditionalAddressFactory
from devices.factories import DeviceFactory
from employees.factories import EmployeeFactory
from services.factories import ServiceFactory


DEVICES = [
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


class OrderServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderService

    service = factory.SubFactory(ServiceFactory)
    name = factory.LazyAttribute(lambda x: faker.sentence(10))
    price_net = factory.LazyAttribute(lambda x: round(random.uniform(0.1, 6000.0), 2))
    quantity = factory.LazyAttribute(lambda x: random.randrange(1, 200))
    is_active = factory.LazyAttribute(lambda x: random.randrange(0, 2))


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name = factory.Sequence(lambda n: f'Region-{n}')


class ShortDescriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShortDescription

    name = factory.Sequence(lambda n: f'Short Descripton-{n}')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user_intake = factory.SubFactory(EmployeeFactory)
    executor = factory.SubFactory(EmployeeFactory)
    approver = factory.SubFactory(EmployeeFactory)
    customer = factory.SubFactory(CustomerFactory)
    phone_number = factory.LazyAttribute(lambda x: random.randrange(10**8, 10**9))
    additional_address = factory.SubFactory(AdditionalAddressFactory)
    payer = None
    region = factory.SubFactory(RegionFactory)
    invoice_number = factory.Sequence(lambda n: f'Invoice-{n}')
    short_description = factory.SubFactory(ShortDescriptionFactory)
    additional_info = factory.LazyAttribute(lambda x: faker.sentence(20))
    priority = factory.LazyAttribute(lambda x: random.randrange(0, 3))
    device_name = factory.LazyAttribute(lambda x: random.choice(DEVICES))
    device = factory.SubFactory(DeviceFactory)
    description = factory.LazyAttribute(lambda x: faker.sentence(10))
    order_type = factory.LazyAttribute(lambda x: random.randrange(0, 10))
    status = factory.LazyAttribute(lambda x: random.randrange(0, 11))
    total_counter = factory.LazyAttribute(lambda x: random.randrange(0, 10**6))
    mono_counter = None
    color_counter = None
    payment_method = factory.LazyAttribute(lambda x: random.randrange(0, 3))
    created_at = factory.LazyFunction(faker.date_time_this_month)
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(seconds=faker.pyint()))
    signer_name = factory.LazyAttribute(lambda x: faker.name())
    latitude = None
    longitude = None

    @post_generation
    def post(self, create, extracted, **kwargs):
        if self.payer is None:
            self.payer = self.customer
        if self.mono_counter is None or self.color_counter is None:
            if self.total_counter is not None:
                self.mono_counter = self.total_counter - random.randint(0, self.total_counter)
                self.color_counter = self.total_counter - self.mono_counter


# todo test order review!!!!!!!!
