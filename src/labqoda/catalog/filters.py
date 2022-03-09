import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter()
    category__slug = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = [
            "name",
            "category__slug",
        ]
