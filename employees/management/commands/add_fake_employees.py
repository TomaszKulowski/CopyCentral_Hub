from sys import stdout

from django.core.management import BaseCommand

from employees.factories import EmployeeFactory


class Command(BaseCommand):
    help = 'Add fake employees.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of employees to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        EmployeeFactory.create_batch(n)
        stdout.write(f'Successfully created {n} objects.')
