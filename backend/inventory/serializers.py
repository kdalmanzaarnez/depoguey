from rest_framework import serializers

from .models import Product, Stock


class ProductFilterSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=Product.Category.choices, required=False)
    active = serializers.BooleanField(source='is_active', required=False)


class ProductListSerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'is_active', 'available']


class StockSerializer(serializers.ModelSerializer):
    location_code = serializers.CharField(source='location.code', read_only=True)
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Stock
        fields = ['location_code', 'on_hand', 'reserved', 'available']


class ProductDetailSerializer(ProductListSerializer):
    stock = StockSerializer(many=True, read_only=True)
    available = serializers.SerializerMethodField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ['description', 'compatibility', 'price', 'stock']

    def get_available(self, product):
        return sum(row.available for row in product.stock.all())
