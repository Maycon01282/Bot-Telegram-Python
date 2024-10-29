# root/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.category_url')),  # Inclua as URLs do aplicativo de categorias
    path('clients/', include('api.urls.client_url')),  # Inclua as URLs do aplicativo de clientes
    path('message/', include('api.urls.message_url')) # Inclua as URLs do aplicativo de mensagens
]