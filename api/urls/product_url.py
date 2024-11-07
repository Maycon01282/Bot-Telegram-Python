# api/urls/product_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.product_view import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]