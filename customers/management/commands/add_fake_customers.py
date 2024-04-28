from sys import stdout

from django.core.management import BaseCommand

from customers.factories import CustomerFactory


class Command(BaseCommand):
    help = 'Add fake customers.'

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
        CustomerFactory.create_batch(n)
        stdout.write(f'Successfully created {n} objects.')
