from rest_framework import serializers
from django.utils import timezone

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=150)
    body = serializers.CharField(max_length=1000, source='description')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    slug = serializers.SlugField()
    inventory = serializers.IntegerField()
    datetime_created = serializers.DateTimeField(default=timezone.now)


    