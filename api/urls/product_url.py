from django.urls import path
from api.views.product_view import (
    list_products_view,
    create_product_view,
    update_product_view,
    delete_product,
    get_product_view,
    products,
    create_product,
    edit_product
)


urlpatterns = [
    path('', products, name='products'),
    path('list/', list_products_view, name='list_products'),
    path('create/api', create_product_view, name='create_product_api'),
    path('create/', create_product, name='create_product'),
    path('update/<int:pk>/', edit_product, name='edit_product'),
    path('update/<int:pk>/api/', update_product_view, name='update_product_api'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
    path('<int:pk>/', get_product_view, name='get_product'),
]