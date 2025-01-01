from django.shortcuts import render, get_object_or_404
from .models import Product, Discount, Category, Comment, Customer, Address, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
        if product.order_items.count() > 0 : 
            return Response({'errors': 'Please delete order items first.'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)
    
    

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0 : 
            return Response({'errors': 'Please delete products first.'}, 
                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)
    

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related('product').all()



# class ProductList(ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()

#     def get_serializer_context(self):
#         return {'request': self.request}


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('category').all()

#     def delete(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0 : 
#             return Response({'errors': 'Please delete order items first.'}, 
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)

    

# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
    

# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.prefetch_related('products').all()
    
#     def delete(self, request, pk):
#         category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
#         if category.products.count() > 0 : 
#             return Response({'errors': 'Please delete products first.'}, 
#                              status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)
    
    

# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def patch(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
#         if product.order_items.count() > 0 : 
#             return Response({'errors': 'Please delete order items first.'}, 
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)
    
    

    
# @api_view(['Get', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method == 'PATCH':
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         if product.order_items.count() > 0 : 
#             return Response({'errors': 'Please delete order items first.'}, 
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.select_related('category').all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data)



# @api_view(['GET', 'POST'])
# def category_list(request): 
#     if request.method == 'GET':
#         category = Category.objects.prefetch_related('products').all()
#         serializer = CategorySerializer(category, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['Get', 'PUT', 'PATCH', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
    
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'PATCH':
#         serializer = CategorySerializer(category, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'DELETE':
#         if category.products.count() > 0 : 
#             return Response({'errors': 'Please delete products first.'}, 
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         category.delete()
#         return Response('Object was deleted.', status=status.HTTP_204_NO_CONTENT)
    