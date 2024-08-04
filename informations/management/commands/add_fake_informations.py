from sys import stdout

from django.core.management import BaseCommand

from informations.factories import InformationFactory


class Command(BaseCommand):
    help = 'Add fake informations.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of informations to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        InformationFactory.create_batch(n)
        stdout.write(f'Successfully created {n} informations.')
