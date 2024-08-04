from sys import stdout

from django.core.management import BaseCommand

from notifications.factories import NotificationFactory


class Command(BaseCommand):
    help = 'Add fake notifications.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of notifications to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        NotificationFactory.create_batch(n)
        stdout.write(f'Successfully created {n} notifications.')
