from rest_framework import serializers

from .models import Product


class ProductFilterSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=Product.Category.choices, required=False)
    active = serializers.BooleanField(source='is_active', required=False)


class ProductListSerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'is_active', 'available']
