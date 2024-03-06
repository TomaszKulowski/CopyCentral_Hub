from sys import stdout

from django.core.management import BaseCommand

from contractors.factories import ContractorFactory


class Command(BaseCommand):
    help = 'Add fake contractors.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of contractors to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        ContractorFactory.create_batch(n)
        stdout.write(f'Successfully created {n} contractors.')
