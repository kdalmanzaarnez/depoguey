from django.db.models import F, Sum
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from accounts.permissions import HasWmsRole

from .models import Product
from .serializers import ProductFilterSerializer, ProductListSerializer


class ProductListView(ListAPIView):
    permission_classes = [HasWmsRole]
    serializer_class = ProductListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'sku']
    queryset = Product.objects.annotate(
        available=Sum(F('stock__on_hand') - F('stock__reserved'), default=0),
    ).order_by('sku')

    def get_queryset(self):
        params = {key: value for key, value in self.request.query_params.items() if value != ''}
        filters = ProductFilterSerializer(data=params)
        filters.is_valid(raise_exception=True)
        return super().get_queryset().filter(**filters.validated_data)
