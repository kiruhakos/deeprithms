from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=config('SU_USERNAME'),
                password=config('SU_PASSWORD')
            )
        print('Superuser has been successfully created.')