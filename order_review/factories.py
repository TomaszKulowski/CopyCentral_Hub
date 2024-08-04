import random

import factory

from django.contrib.auth import get_user_model
from faker import Faker

from .models import OrderReview
from orders.factories import OrderFactory

faker = Faker()
User = get_user_model()


class OrderReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderReview

    user = factory.LazyAttribute(lambda x: User.objects.filter(employee__department__lt=3).order_by('?').first())
    order = factory.LazyAttribute(lambda x: OrderFactory(status=random.randint(2, 5)))
    is_approved = factory.LazyAttribute(lambda x: random.choice([True, False]))
    for_review = factory.LazyAttribute(lambda x: random.choice([True, False]))
