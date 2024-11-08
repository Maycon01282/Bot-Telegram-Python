from django.urls import path
from api.views.client_view import (
    list_clients_view, get_client_view, create_client_view,
    update_client_view, delete_client_view, clients, client_edit_page
)

urlpatterns = [
    path('', clients, name='clients'),  # Main page for clients
    path('list/', list_clients_view, name='list_clients'),  # URL for listing clients with pagination
    path('<int:client_id>/', get_client_view, name='get_client'),
    path('create/', create_client_view, name='create_client'),
    path('update/<int:client_id>/', update_client_view, name='update_client'),
    path('delete/<int:client_id>/', delete_client_view, name='delete_client'),
]