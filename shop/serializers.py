from rest_framework import serializers
from django.utils import timezone
from decimal import Decimal

from .models import Product, Category


DOLLAR_TO_RIAL = 800000


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        
    name = serializers.CharField(max_length=150, source='title')



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','body','category','price','slug','inventory','datetime_created','rial_price','price_with_tax']
    
    body = serializers.CharField(max_length=1000, source='description')
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all() ,
        view_name='category_detail'
    ) 
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    rial_price = serializers.SerializerMethodField()
    price_with_tax = serializers.SerializerMethodField(method_name='calc_tat')
    
    def calc_tat(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
        
    def get_rial_price(self, product):
        return int(product.unit_price * DOLLAR_TO_RIAL)
    


    