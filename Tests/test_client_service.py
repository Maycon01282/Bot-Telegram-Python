# In your urls.py
from django.urls import path
from api.views.client_view import get_client_view

urlpatterns = [
    path('clients/<int:client_id>/', get_client_view, name='get_client_by_id'),
]