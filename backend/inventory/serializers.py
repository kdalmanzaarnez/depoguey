from rest_framework import serializers

from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'is_active', 'available']
