from sys import stdout

from django.core.management import BaseCommand

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
        ServiceOrderFactory.create_batch(n)
        stdout.write(f'Successfully created {n} objects.')
