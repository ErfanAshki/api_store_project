from rest_framework import serializers
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal

from .models import Product, Category, Comment, Order, OrderItem, Cart, CartItem


DOLLAR_TO_RIAL = 800000


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'number_of_products']
        
    name = serializers.CharField(max_length=150, source='title')
    number_of_products = serializers.SerializerMethodField()

    
    def get_number_of_products(self, category):
        return category.products.count()
    
    def validate(self, data):
        title = data.get('title')
        if title:
            if len(data['title']) < 3:
                raise serializers.ValidationError('Too short title')
        return data
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','body', 'category', 'price', 'inventory', 'datetime_created', 'rial_price', 'price_with_tax']
    
    body = serializers.CharField(max_length=1000, source='description')
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all() ,
    #     view_name='category_detail'
    # ) 
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    rial_price = serializers.SerializerMethodField()
    price_with_tax = serializers.SerializerMethodField(method_name='calc_tat')
    
    def calc_tat(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
        
    def get_rial_price(self, product):
        return int(product.unit_price * DOLLAR_TO_RIAL)
    
    def validate(self, data):
        name = data.get('name')
        if name:
            if len(data['name']) < 5 :
                raise serializers.ValidationError('Too short name')
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    
    # def update(self, validated_data, instance):
    #     instance.inventory = validated_data.get('inventory')
    #     instance.save()
    #     return instance
    
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'name', 'status', 'datetime_created']
        
    text = serializers.CharField(max_length=500, source='body')
    
    def validate(self, data):
        body = data.get('body')
        if body:
            if len(data['body']) < 4 :
                raise serializers.ValidationError('Too short comment')
        return data  
    
    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.product_id = self.context['product_pk']
        comment.save()
        return comment
    
    # way two
    # def create(self, validated_data):
    #     product_pk = self.context['product_pk']
    #     return Comment.objects.create(product_id=product_pk, **validated_data)
    

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_price']
        read_only_fields = ['cart']
        
    product = CartItemProductSerializer()
    item_price = serializers.SerializerMethodField()
    
    def get_item_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price
        

        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id' ,'number_of_items', 'total_price', 'items']
        read_only_fields = ['id', 'items']
        
    number_of_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True)
    
    def get_number_of_items(self, cart):
        return cart.items.count()
    
    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())
