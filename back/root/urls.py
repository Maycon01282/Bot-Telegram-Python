"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.category_url')),  # Inclua as URLs do aplicativo de categorias
    path('clients/', include('api.urls.client_url')),  # Inclua as URLs do aplicativo de clientes
    path('message/', include('api.urls.message_url')),  # Inclua as URLs do aplicativo de mensagens
    path('order/', include('api.urls.order_url')),  # Inclua as URLs do aplicativo de pedidos
    path('order_item/', include('api.urls.order_item_url')),  # Inclua as URLs do aplicativo de itens de pedidos
    path('products/', include('api.urls.product_url')),  # Inclua as URLs do aplicativo de produtos
    path('users/', include('api.urls.user_url'))  # Inclua as URLs do aplicativo de usuários
]