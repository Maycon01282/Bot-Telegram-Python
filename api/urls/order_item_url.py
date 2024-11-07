# api/urls/order_item_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.order_item_view import OrderItemViewSet

router = DefaultRouter()
router.register(r'order_items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]