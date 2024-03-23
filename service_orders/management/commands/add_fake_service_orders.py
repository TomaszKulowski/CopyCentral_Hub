from sys import stdout

from django.core.management import BaseCommand

from customers.factories import CustomerFactory, AdditionalAddressFactory
from orders.factories import OrderFactory
from service_orders.factories import ServiceOrderFactory


class Command(BaseCommand):
    help = 'Add fake service orders.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of service orders to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        for _ in range(int(n)):
            customer = CustomerFactory()
            additional_address = AdditionalAddressFactory(customer=customer)
            order = OrderFactory(customer=customer, additional_address=additional_address)
            ServiceOrderFactory(order=order)
        stdout.write(f'Successfully created {n} objects.')
