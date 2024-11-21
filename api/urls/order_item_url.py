from django.urls import path
from api.views.order_item_view import create_order_item_view, get_order_item_view, update_order_item_view, delete_order_item_view, list_order_items_view

urlpatterns = [
    path('order_items/create/', create_order_item_view, name='create_order_item'),
    path('order_items/<int:order_item_id>/', get_order_item_view, name='get_order_item'),
    path('order_items/update/<int:order_item_id>/', update_order_item_view, name='update_order_item'),
    path('order_items/delete/<int:order_item_id>/', delete_order_item_view, name='delete_order_item'),
    path('order_items/order/<int:order_id>/', list_order_items_view, name='list_order_items'),
]