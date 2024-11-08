from django.urls import path
from api.views.order_view import (
    list_orders_view,
    get_order_view,
    create_order_view,
    update_order_view,
    delete_order_view,
    orders
)

urlpatterns = [
    path('', orders, name="orders"),
    path('create/', create_order_view, name='create_order'),
    path('<int:order_id>/', get_order_view, name='get_order_by_id'),
    path('update/<int:order_id>/', update_order_view, name='update_order'),
    path('delete/<int:order_id>/', delete_order_view, name='delete_order'),
    path('list/', list_orders_view, name='list_orders'), 
]