from django.urls import path
from api.views.client_view import list_clients_view, get_client_view, create_client_view, update_client_view, delete_client_view

urlpatterns = [
    path('clients/', list_clients_view, name='list_clients'),
    path('clients/<int:client_id>/', get_client_view, name='get_client'),
    path('clients/create/', create_client_view, name='create_client'),
    path('clients/update/<int:client_id>/', update_client_view, name='update_client'),
    path('clients/delete/<int:client_id>/', delete_client_view, name='delete_client'),
]
