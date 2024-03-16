import random

from datetime import timedelta

import factory

from factory import post_generation
from faker import Faker

from .models import OrderServices, Region, ShortDescription, Order
from customers.factories import CustomerFactory, AdditionalAddressFactory
from devices.factories import DeviceFactory
from employees.factories import EmployeeFactory
from services.factories import ServiceFactory


faker = Faker()


class OrderServicesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderServices

    service = factory.SubFactory(ServiceFactory)
    price_net = factory.LazyAttribute(lambda x: round(random.uniform(1.1, 6000.0), 2))
    quantity = factory.LazyAttribute(lambda x: random.randrange(1, 200))


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
    additional_address = factory.SubFactory(AdditionalAddressFactory)
    payer = None
    region = factory.SubFactory(RegionFactory)
    invoice_number = factory.Sequence(lambda n: f'Invoice-{n}')
    short_description = factory.SubFactory(ShortDescriptionFactory)
    additional_info = factory.LazyAttribute(lambda x: faker.sentence(20))
    priority = factory.LazyAttribute(lambda x: random.randrange(0, 3))
    device = factory.SubFactory(DeviceFactory)
    payment_method = factory.LazyAttribute(lambda x: random.randrange(0, 3))
    created_at = factory.LazyFunction(faker.date_time_this_month)
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(seconds=faker.pyint()))

    @post_generation
    def post(self, create, *args, **kwargs):
        self.payer = self.customer
