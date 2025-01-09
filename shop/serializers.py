from rest_framework import serializers
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Product, Category, Comment, Order, OrderItem, Cart, CartItem, Customer


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
        

class CartItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity']

    def create(self, validated_data):
        
        cart_pk = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_pk, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem(**validated_data)
            cart_item.cart_id = self.context['cart_pk']
            cart_item.save()
        
        self.instance = cart_item
        return cart_item
        

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id' ,'number_of_items', 'total_price', 'items']
        read_only_fields = ['id', 'items']
        
    number_of_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)
    
    def get_number_of_items(self, cart):
        return cart.items.count()
    
    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Customer
        fields = ['id', 'user', 'phone_number', 'birth_date', 'email', 'number_of_orders']
        read_only_fields = ['user']
        
    number_of_orders = serializers.SerializerMethodField()

    def get_number_of_orders(self, customer):
        return customer.orders.count()
    


class ProductForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:    
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']
        
        product = ProductSerializer()



# class UserForCustomerOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'last_name']


class CustomerForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']    
        
    # user = UserForCustomerOrderSerializer()
    first_name = serializers.CharField(max_length=250, source='user.first_name')
    last_name = serializers.CharField(max_length=250, source='user.last_name')
    


class OrderForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'number_of_items', 'items']
        
    number_of_items = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True)
    customer = CustomerForOrderSerializer()

    def get_number_of_items(self, order):
        return order.items.count()


class OrderForUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'number_of_items', 'items']
        
    number_of_items = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True)

    def get_number_of_items(self, order):
        return order.items.count()
    

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('There is no cart with this id .')
        
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('This cart is empty , please add some products to it first .')
        
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id).all()
            
            order_items = list()
            for cart_item in cart_items:
                order_item = OrderItem()
                order_item.order = order
                order_item.product = cart_item.product
                order_item.quantity = cart_item.quantity
                order_item.unit_price = cart_item.product.unit_price

                order_items.append(order_item)
            
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.get(id=cart_id).delete()
            
            return order
    
    
    
        # cart = Cart.objects.prefetch_related('items').get(id=cart_id)
        
        # for item in cart.items.all():
        #     OrderItem.objects.create(
        #     order=order,
        #     product=item.product,
        #     quantity=item.quantity,
        #     unit_price=item.product.unit_price
        #     )
        