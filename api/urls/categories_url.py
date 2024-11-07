# api/urls/categories_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.category_view import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]