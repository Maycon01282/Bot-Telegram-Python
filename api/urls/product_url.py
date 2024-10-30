from django.urls import path
from api.views.product_view import product_list_view, product_detail_view, product_create_view, product_update_view, product_delete_view
from admin_panel.views import products

urlpatterns = [
    path('', products, name='products'),
    path('products/', product_list_view, name='product_list'),  # URL for listing products with pagination
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('products/create/', product_create_view, name='product_create'),
    path('products/<int:product_id>/update/', product_update_view, name='product_update'),
    path('products/<int:product_id>/delete/', product_delete_view, name='product_delete'),
]