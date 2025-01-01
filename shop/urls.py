from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('category', views.CategoryViewSet, basename='category')
router.register('comment', views.Co, basename='comment')

urlpatterns = router.urls 


