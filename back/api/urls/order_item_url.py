from django.urls import path
from api.views.order_item_view import create_order_item, get_order_item_by_id, update_order_item, delete_order_item, list_order_items_by_order

urlpatterns = [
    path('order_item/create/', create_order_item, name='create_order_item'),
    path('order_item/<int:order_item_id>/', get_order_item_by_id, name='get_order_item_by_id'),
    path('order_item/update/<int:order_item_id>/', update_order_item, name='update_order_item'),
    path('order_item/delete/<int:order_item_id>/', delete_order_item, name='delete_order_item'),
    path('order/<int:order_id>/order_items/', list_order_items_by_order, name='list_order_items_by_order'),
]