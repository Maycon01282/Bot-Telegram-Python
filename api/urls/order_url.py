# api/urls/order_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.order_view import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]