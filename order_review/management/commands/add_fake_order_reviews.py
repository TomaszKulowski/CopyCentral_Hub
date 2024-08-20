import random

from sys import stdout
from unittest.mock import patch

from django.core.management import BaseCommand

from order_review.factories import OrderReviewFactory


class Command(BaseCommand):
    help = 'Add fake orders to review.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of orders to review to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        with patch('orders.locations.get_coordinates') as mock_update_coordinates:
            for _ in range(n):
                mock_update_coordinates.return_value = (
                    round(random.uniform(-90.0, 90.0), 6),
                    round(random.uniform(-180.0, 180.0), 6),
                )
                OrderReviewFactory()
        stdout.write(f'Successfully created {n} objects.')
