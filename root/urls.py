# root/urls.py

from django.contrib import admin
from django.urls import include, path
from api.views.category_view import CategoryViewSet
from rest_framework.routers import DefaultRouter
from utils.swagger.swagger_views import urlpatterns as swagger_urls  # Import swagger_view urlpatterns

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include('api.urls.home_url'), name='home'),
    path('login/', include('api.urls.auth_url'), name='login'),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.categories_url')),  # Include category URLs
    path('clients/', include('api.urls.client_url')),  # Include client URLs
    path('message/', include('api.urls.message_url')),  # Include message URLs
    path('order/', include('api.urls.order_url')),  # Include order URLs
    path('order_item/', include('api.urls.order_item_url')),  # Include order item URLs
    path('products/', include('api.urls.product_url')),  # Include product URLs
    path('users/', include('api.urls.user_url')),  # Include user URLs
    path('', include(swagger_urls)),  # Include the swagger_view URLs
]