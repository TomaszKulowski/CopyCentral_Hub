from sys import stdout

from django.core.management import BaseCommand

from orders.factories import OrderFactory


class Command(BaseCommand):
    help = 'Add fake orders.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of orders to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        OrderFactory.create_batch(n)
        stdout.write(f'Successfully created {n} objects.')
