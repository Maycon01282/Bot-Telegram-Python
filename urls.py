# root/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('api.urls.home_url'), name='home'),
    path('login/', include('api.urls.auth_url'), name='login'),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.category_url')),  # Inclua as URLs do aplicativo de categorias
    path('clients/', include('api.urls.client_url')),  # Inclua as URLs do aplicativo de clientes
    path('message/', include('api.urls.message_url')), # Inclua as URLs do aplicativo de mensagens
    path('message/', include('api.urls.message_url')),  # Inclua as URLs do aplicativo de mensagens
    path('order/', include('api.urls.order_url')),  # Inclua as URLs do aplicativo de pedidos
    path('order_item/', include('api.urls.order_item_url')),  # Inclua as URLs do aplicativo de itens de pedidos
    path('products/', include('api.urls.product_url')),  # Inclua as URLs do aplicativo de produtos
    path('users/', include('api.urls.user_url')),  # Inclua as URLs do aplicativo de usuários
]