from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('home/', include('api.urls.home_url'), name='home'),
    path('register/', include('api.urls.user_url')),
    path('', include('api.urls.auth_url'), name='login'),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.categories_url')),  
    path('clients/', include('api.urls.client_url')),  
    path('message/', include('api.urls.message_url')),  
    path('orders/', include('api.urls.order_url')),  
    path('order_item/', include('api.urls.order_item_url')),  
    path('products/', include('api.urls.product_url')),  
    path('users/', include('api.urls.user_url')),  
]
