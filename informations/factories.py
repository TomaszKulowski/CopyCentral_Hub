import factory

from faker import Faker

from .models import Information


faker = Faker()


class InformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Information

    information = factory.LazyAttribute(lambda x: faker.sentence(10))
