from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.db import DataError, IntegrityError, transaction
from django.test import TestCase

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
