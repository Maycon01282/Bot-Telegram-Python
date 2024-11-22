# api/urls/order_item_url.py
from django.urls import path
from api.views.order_item_view import create_order_item_view, get_order_item_view, update_order_item_view, delete_order_item_view, list_order_items_view

urlpatterns = [
    path('create/', create_order_item_view, name='create_order_item'),
    path('<int:order_item_id>/', get_order_item_view, name='get_order_item'),
    path('update/<int:order_item_id>/', update_order_item_view, name='update_order_item'),
    path('delete/<int:order_item_id>/', delete_order_item_view, name='delete_order_item'),
    path('order/<int:order_id>/', list_order_items_view, name='list_order_items'),
]