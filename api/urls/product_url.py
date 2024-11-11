# api/urls/product_url.py
from django.urls import path
from api.views.product_view import (
    list_products_view,
    create_product_view,
    products,
    update_product_view,
    delete_product_view,
    get_product_view,
    list_products_by_category,
    delete_product
)

urlpatterns = [
    path('', products, name='products'),
    path('list/', list_products_view, name='list_products'),
    path('create/', create_product_view, name='create_product'),
    path('update/<int:pk>/', update_product_view, name='update_product'),
    path('delete/<int:pk>/', delete_product_view, name='delete_product'),
    path('<int:pk>/', get_product_view, name='get_product'),
    path('category/<int:category_id>/', list_products_by_category, name='list_products_by_category'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
]