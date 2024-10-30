from django.contrib import admin
from django.urls import path,include
from admin_panel.views import login,home, orders, clients, users, products, category
from api.views.auth_view import login_view

urlpatterns = [
    path('', login, name="index"),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.category_url')),  # Inclua as URLs do aplicativo de categorias
    path('clients/', include('api.urls.client_url')),  # Inclua as URLs do aplicativo de clientes
    path('message/', include('api.urls.message_url')),  # Inclua as URLs do aplicativo de mensagens
    path('login/', login, name='login_html'),
    path('order/', include('api.urls.order_url')),  # Inclua as URLs do aplicativo de pedidos
    path('order_item/', include('api.urls.order_item_url')),  # Inclua as URLs do aplicativo de itens de pedidos
    path('products/', include('api.urls.product_url')),  # Inclua as URLs do aplicativo de produtos
    path('users/', include('api.urls.user_url')),  # Inclua as URLs do aplicativo de usuários
    path('login/', login_view, name='login_html'),
    path('home/', home, name='home_html'),
    path('orders/', orders, name='orders_html'),
    path('clients/', clients, name='clients_html'),
    path('users/', users, name='users_html'),
    path('products/', products, name='products_html'),
    path('category/', category, name='category_html')
]
