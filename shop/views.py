from django.shortcuts import render, get_object_or_404
from .models import Product, Discount, Category, Comment, Customer, Address, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view()
def product_list(request):
    products = Product.objects.select_related('category').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
