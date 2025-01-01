from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


router = SimpleRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('category', views.CategoryViewSet, basename='category')

urlpatterns = router.urls 


