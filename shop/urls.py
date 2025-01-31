from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('category', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('orders', views.OrderViewSet, basename='order')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('comments', views.CommentViewSet, basename='product_comment')

cart_item_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_item_router.register('items', views.CartItemViewSet, basename='cart_item')


urlpatterns = router.urls + product_router.urls + cart_item_router.urls 

