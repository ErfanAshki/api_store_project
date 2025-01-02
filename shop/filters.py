from .models import Product

from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category']
        
    inventory_range = filters.RangeFilter(field_name="inventory", label='enter inventory_range')
    
    # category_title = filters.CharFilter(method="filter_by_category", label='category title ')
    
    # def filter_by_category(self, queryset, name, value):
    #     return queryset.filter(category__title=value)

