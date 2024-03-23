import random

import factory

from factory import post_generation
from faker import Faker

from .models import ServiceOrder
from orders.factories import OrderFactory

from customers.factories import AdditionalAddressFactory


faker = Faker()


class ServiceOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServiceOrder

    order = factory.SubFactory(OrderFactory)
    description = factory.LazyAttribute(lambda x: faker.sentence(10))
    order_type = factory.LazyAttribute(lambda x: random.randrange(0, 10))
    status = factory.LazyAttribute(lambda x: random.randrange(0, 9))
    total_counter = factory.LazyAttribute(lambda x: random.randrange(0, 10**6))
    mono_counter = None
    color_counter = None

    @post_generation
    def post(self, create, *args, **kwargs):
        self.mono_counter = self.total_counter - random.randint(0, self.total_counter)
        self.color_counter = self.total_counter - self.mono_counter
