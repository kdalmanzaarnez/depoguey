import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from accounts.roles import ADMIN, EMPLOYEE

DEMO_USERS = [
    {'username': 'medewerker', 'first_name': 'Demo', 'last_name': 'Medewerker', 'role': EMPLOYEE, 'is_staff': False},
    {'username': 'admin', 'first_name': 'Demo', 'last_name': 'Admin', 'role': ADMIN, 'is_staff': True},
]


class Command(BaseCommand):
    help = 'Maakt de demogebruikers aan of zet ze terug naar hun beginstand.'

    def handle(self, *args, **options):
        password = os.environ.get('DEMO_PASSWORD')
        if not password:
            raise CommandError('DEMO_PASSWORD ontbreekt in .env.')

        User = get_user_model()
        for data in DEMO_USERS:
            group = Group.objects.get(name=data['role'])
            user, created = User.objects.update_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_staff': data['is_staff'],
                    'is_active': True,
                },
            )
            user.set_password(password)
            user.save()
            user.groups.set([group])

            action = 'aangemaakt' if created else 'bijgewerkt'
            self.stdout.write(f"{data['username']} ({data['role']}) {action}")
