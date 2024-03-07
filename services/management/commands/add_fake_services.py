from sys import stdout

from django.core.management import BaseCommand

from services.factories import ServiceFactory


class Command(BaseCommand):
    help = 'Add fake services.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of services to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        ServiceFactory.create_batch(n)
        stdout.write(f'Successfully created {n} objects.')
