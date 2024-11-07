# api/urls/message_url.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.message_view import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]