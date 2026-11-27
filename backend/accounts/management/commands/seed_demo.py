import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.roles import ADMIN, EMPLOYEE
from inventory.models import Location, Product, Stock

DEMO_USERS = [
    {'username': 'medewerker', 'first_name': 'Demo', 'last_name': 'Medewerker', 'role': EMPLOYEE, 'is_staff': False},
    {'username': 'admin', 'first_name': 'Demo', 'last_name': 'Admin', 'role': ADMIN, 'is_staff': True},
]


class Command(BaseCommand):
    help = 'Zet demogebruikers terug naar hun beginstand en voegt demoproducten met beginvoorraad toe.'

    @transaction.atomic
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

        headset, created = Product.objects.get_or_create(
            sku='DEMO-HS-01',
            defaults={
                'name': 'Stereoheadset', 'category': Product.Category.HEADSET,
                'compatibility': 'PC, PS5', 'price': '49.95',
            },
        )
        # Beginvoorraad hoort alleen bij de eerste aanleg van dit demoproduct.
        if created:
            for code, quantity in [('A-01', 10), ('A-02', 5)]:
                location, _ = Location.objects.get_or_create(code=code)
                Stock.objects.create(product=headset, location=location, on_hand=quantity)

        Product.objects.get_or_create(
            sku='DEMO-MS-01',
            defaults={
                'name': 'Gamingmuis', 'category': Product.Category.MOUSE,
                'compatibility': 'PC', 'price': '24.95', 'is_active': False,
            },
        )
        self.stdout.write('Demoproducten gereed.')
