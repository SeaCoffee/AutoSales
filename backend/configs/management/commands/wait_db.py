import time

from django.core.management import BaseCommand
from django.db import OperationalError, connection


class Command(BaseCommand):
    help = 'Waits until the database is available.'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')

        while True:
            try:
                connection.ensure_connection()
                break
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 3 seconds...')
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS('Database is available.'))