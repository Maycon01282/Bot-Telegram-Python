from django.urls import path
from . import views  # Usar 'views' ao invés de 'client_url'

urlpatterns = [
    path('clients/', views.list_clients, name='list_clients'),
    path('clients/<int:client_id>/', views.get_client, name='get_client'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/update/<int:client_id>/', views.update_client, name='update_client'),
    path('clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),
]
