from django.db.models import F, Sum
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.permissions import HasWmsRole

from .models import Product
from .serializers import ProductListSerializer


class ProductListView(ListAPIView):
    permission_classes = [HasWmsRole]
    serializer_class = ProductListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'sku']
    queryset = Product.objects.annotate(
        available=Sum(F('stock__on_hand') - F('stock__reserved'), default=0),
    ).order_by('sku')
