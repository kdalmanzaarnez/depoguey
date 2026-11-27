from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.db import DataError, IntegrityError, transaction
from django.test import TestCase

from accounts.roles import ADMIN, EMPLOYEE

from .models import Location, Product, Stock


class StockTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            sku='HS-01', name='Headset', category=Product.Category.HEADSET, price=49,
        )
        cls.location = Location.objects.create(code='A-01')

    def test_available_is_on_hand_minus_reserved(self):
        stock = Stock.objects.create(product=self.product, location=self.location, on_hand=10, reserved=3)
        self.assertEqual(stock.available, 7)

        stock.reserved = stock.on_hand
        stock.save(update_fields=['reserved'])
        self.assertEqual(stock.available, 0)

    def test_stock_is_unique_per_product_and_location(self):
        Stock.objects.create(product=self.product, location=self.location)
        Stock.objects.create(product=self.product, location=Location.objects.create(code='A-02'))
        mouse = Product.objects.create(sku='MS-01', name='Muis', category=Product.Category.MOUSE, price=25)
        Stock.objects.create(product=mouse, location=self.location)

        with self.assertRaises(IntegrityError), transaction.atomic():
            Stock.objects.create(product=self.product, location=self.location)

    def test_cannot_reduce_on_hand_below_reserved(self):
        stock = Stock.objects.create(product=self.product, location=self.location, on_hand=3, reserved=3)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Stock.objects.filter(pk=stock.pk).update(on_hand=2)

    def test_quantities_cannot_be_negative(self):
        for on_hand, reserved in [(-1, 0), (3, -1)]:
            with self.subTest(on_hand=on_hand, reserved=reserved):
                with self.assertRaises((DataError, IntegrityError)), transaction.atomic():
                    Stock.objects.create(
                        product=self.product, location=self.location, on_hand=on_hand, reserved=reserved,
                    )


class DemoInventoryTests(TestCase):
    @patch.dict('os.environ', {'DEMO_PASSWORD': 'test-wachtwoord-123'})
    def test_seed_demo_creates_stock_once(self):
        call_command('seed_demo', stdout=StringIO())

        headset = Product.objects.get(sku='DEMO-HS-01', is_active=True)
        self.assertTrue(Product.objects.filter(sku='DEMO-MS-01', is_active=False).exists())
        self.assertEqual(dict(headset.stock.values_list('location__code', 'on_hand')), {'A-01': 10, 'A-02': 5})

        headset.stock.filter(location__code='A-01').update(on_hand=8, reserved=2)
        call_command('seed_demo', stdout=StringIO())

        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(Stock.objects.count(), 2)
        stock = headset.stock.get(location__code='A-01')
        self.assertEqual((stock.on_hand, stock.reserved), (8, 2))


class ProductListTests(TestCase):
    url = '/api/products/'

    def login_as_employee(self):
        user = get_user_model().objects.create_user(username='medewerker')
        user.groups.add(Group.objects.get(name=EMPLOYEE))
        self.client.force_login(user)

    def test_employee_and_admin_can_read_products_with_available_stock(self):
        mouse = Product.objects.create(
            sku='MS-01', name='Muis', category=Product.Category.MOUSE, price=25, is_active=False,
        )
        headset = Product.objects.create(
            sku='HS-01', name='Headset', category=Product.Category.HEADSET, price=49,
        )
        Stock.objects.create(product=headset, location=Location.objects.create(code='A-01'), on_hand=10, reserved=3)
        Stock.objects.create(product=headset, location=Location.objects.create(code='A-02'), on_hand=5, reserved=1)

        for role in (EMPLOYEE, ADMIN):
            with self.subTest(role=role):
                user = get_user_model().objects.create_user(username=role)
                user.groups.add(Group.objects.get(name=role))
                self.client.force_login(user)
                response = self.client.get(self.url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), [
                    {'id': headset.pk, 'sku': 'HS-01', 'name': 'Headset', 'category': 'headset',
                     'is_active': True, 'available': 11},
                    {'id': mouse.pk, 'sku': 'MS-01', 'name': 'Muis', 'category': 'mouse',
                     'is_active': False, 'available': 0},
                ])

    def test_anonymous_user_is_denied(self):
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_user_without_wms_role_is_denied(self):
        self.client.force_login(get_user_model().objects.create_user(username='zonder-rol'))
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_search_by_partial_name_or_sku(self):
        Product.objects.create(sku='HS-01', name='Stereoheadset', category=Product.Category.HEADSET, price=49)
        Product.objects.create(sku='MS-02', name='Gamingmuis', category=Product.Category.MOUSE, price=25)
        self.login_as_employee()

        for term, expected_skus in [
            ('HEAD', ['HS-01']),
            ('ms-0', ['MS-02']),
            ('toetsenbord', []),
            ('', ['HS-01', 'MS-02']),
        ]:
            with self.subTest(term=term):
                response = self.client.get(self.url, {'search': term})
                self.assertEqual(response.status_code, 200)
                self.assertEqual([product['sku'] for product in response.json()], expected_skus)

    def test_filters_by_category_and_status_with_optional_search(self):
        Product.objects.create(sku='HS-01', name='Gamingheadset', category=Product.Category.HEADSET, price=49)
        Product.objects.create(
            sku='HS-02', name='Studioheadset', category=Product.Category.HEADSET, price=59, is_active=False,
        )
        Product.objects.create(sku='MS-01', name='Gamingmuis', category=Product.Category.MOUSE, price=25)
        self.login_as_employee()

        for params, expected_skus in [
            ({'category': 'headset'}, ['HS-01', 'HS-02']),
            ({'active': 'true'}, ['HS-01', 'MS-01']),
            ({'active': 'false'}, ['HS-02']),
            ({'category': 'headset', 'active': 'true', 'search': 'gaming'}, ['HS-01']),
            ({'category': 'headset', 'active': 'true', 'search': 'studio'}, []),
            ({'category': '', 'active': ''}, ['HS-01', 'HS-02', 'MS-01']),
        ]:
            with self.subTest(params=params):
                response = self.client.get(self.url, params)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([product['sku'] for product in response.json()], expected_skus)

    def test_invalid_filter_values_return_field_errors(self):
        self.login_as_employee()
        for field in ('category', 'active'):
            with self.subTest(field=field):
                response = self.client.get(self.url, {field: 'onbekend'})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json())
