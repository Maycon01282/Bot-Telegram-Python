# api/urls/categories_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.client_view import ClientViewSet

router = DefaultRouter()
router.register(r'client', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]