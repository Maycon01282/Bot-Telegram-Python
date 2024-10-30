# root/urls.py

from django.contrib import admin
from django.urls import include, path
from admin_panel.views import login, home, orders, clients, users, products, category
from api.views.auth_view import login_view

urlpatterns = [
    path('', login, name="index"),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.category_url')),  # Include category URLs
    path('clients/', include('api.urls.client_url')),  # Include client URLs
    path('message/', include('api.urls.message_url')),  # Include message URLs
    path('login/', login, name='login_html'),
    path('order/', include('api.urls.order_url')),  # Include order URLs
    path('order_item/', include('api.urls.order_item_url')),  # Include order item URLs
    path('products/', include('api.urls.product_url')),  # Include product URLs
    path('users/', include('api.urls.user_url')),  # Include user URLs
    path('login/', login_view, name='login'),
    path('home/', home, name='home_html'),
    path('orders/', orders, name='orders_html'),
    path('clients/', clients, name='clients_html'),
    path('users/', users, name='users_html'),
    path('products/', products, name='products_html'),
    path('category/', category, name='category_html')
]