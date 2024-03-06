from sys import stdout

from django.core.management import BaseCommand

from devices.factories import DeviceFactory


class Command(BaseCommand):
    help = 'Add fake devices.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of devices to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        DeviceFactory.create_batch(n)
        stdout.write(f'Successfully created {n} devices.')
