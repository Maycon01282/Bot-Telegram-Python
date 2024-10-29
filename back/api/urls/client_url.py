from django.urls import path
from api.views.client_view import list_clients, get_client_by_id, create_client, update_client, delete_client


urlpatterns = [
    path('clients/', list_clients, name='list_clients'),
    path('clients/<int:client_id>/', get_client_by_id, name='get_client'),
    path('clients/create/', create_client, name='create_client'),
    path('clients/update/<int:client_id>/', update_client, name='update_client'),
    path('clients/delete/<int:client_id>/', delete_client, name='delete_client'),
]
