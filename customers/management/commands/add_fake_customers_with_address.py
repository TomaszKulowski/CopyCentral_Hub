from sys import stdout

from django.core.management import BaseCommand

from customers.factories import AdditionalAddressFactory, CustomerFactory


class Command(BaseCommand):
    help = 'Add fake customers with additional address.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of customers to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        for _ in range(int(n)):
            customer = CustomerFactory()
            AdditionalAddressFactory(customer=customer)
        stdout.write(f'Successfully created {n} objects.')
