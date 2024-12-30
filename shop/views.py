from django.shortcuts import render
from .models import Product, Discount, Category, Comment, Customer, Address, Cart, CartItem, Order, OrderItem

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def product_list(request):
    return Response('hello')
