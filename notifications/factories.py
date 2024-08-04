import random

import factory

from faker import Faker

from .models import NotificationSettings, Notification

faker = Faker()


class NotificationSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotificationSettings

    server = factory.LazyAttribute(lambda x: faker.ipv4())
    auth_token = factory.Sequence(lambda x: faker.unique.uuid4())
    message_template = factory.LazyAttribute(lambda x: faker.sentence(10))
    notification_type = 0
    delay_time = factory.LazyAttribute(lambda x: random.randrange(0, 10))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        notification_type = kwargs.get('notification_type', 0)
        existing_settings = NotificationSettings.objects.filter(notification_type=notification_type).first()
        if existing_settings:
            return existing_settings
        return super()._create(model_class, *args, **kwargs)


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    settings = factory.SubFactory(NotificationSettingsFactory)
    receiver_name = factory.LazyAttribute(lambda x: f'{faker.first_name()} {faker.last_name()}')
    phone_number = factory.LazyAttribute(lambda x: random.randrange(10**8, 10**9))
    message = factory.LazyAttribute(lambda x: f'You have received a new order with ID {random.randint(0,10**5)}.')
    sent = factory.LazyAttribute(lambda x: random.randrange(0, 2))
    created_at = factory.LazyAttribute(lambda x: faker.date_time_between(start_date='-1y', end_date='now'))
