from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):

    class Category(models.TextChoices):
        HEADSET = 'headset', 'Headset'
        CONTROLLER = 'controller', 'Controller'
        KEYBOARD = 'keyboard', 'Toetsenbord'
        MOUSE = 'mouse', 'Muis'
        OTHER = 'other', 'Overig'

    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=Category.choices)
    description = models.TextField(blank=True)
    # Vrije tekst, bijvoorbeeld "PC, PS5, Xbox Series X|S"
    compatibility = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    is_active = models.BooleanField(default=True)
    # Drempel voor de melding lage voorraad op het dashboard
    min_stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sku']

    def __str__(self):
        return f'{self.sku} · {self.name}'


class Location(models.Model):
    code = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.code


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock')
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    on_hand = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'location'],
                name='stock_unique_product_location',
            ),
            models.CheckConstraint(
                condition=models.Q(reserved__lte=models.F('on_hand')),
                name='stock_reserved_lte_on_hand',
            ),
        ]

    @property
    def available(self):
        return self.on_hand - self.reserved
