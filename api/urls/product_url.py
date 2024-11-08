# api/urls/product_url.py
from django.urls import path
from api.views.product_view import list_products_view, create_product_view, update_product_view, delete_product_view, get_product_view

urlpatterns = [
    path('list/', list_products_view, name='list_products'),
    path('create/', create_product_view, name='create_product'),
    path('update/<int:pk>/', update_product_view, name='update_product'),
    path('delete/<int:pk>/', delete_product_view, name='delete_product'),
    path('<int:pk>/', get_product_view, name='get_product'),
]