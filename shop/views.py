from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Q, F, Avg, Count, Max, Min, Sum, Value, Func,ExpressionWrapper,DecimalField,Prefetch
from django.db import transaction

from .models import Product, Discount, Category, Comment, Customer, Address, Cart, CartItem, Order, OrderItem


def some_view(request):
    queryset = Order.objects.prefetch_related(Prefetch( \
        'items', queryset=OrderItem.objects.select_related('product'))) \
        .annotate(order_items=Count('items'))
    
    return render(request, 'shop/shop.html', {'orders': list(queryset)})
