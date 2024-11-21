from django.urls import path
from api.views.kanban_view import update_order_status
from api.views.order_view import (
    list_orders_view,
    get_order_view,
    create_order_view,
    delete_order_view,
    orders,
    edit_order_page,
    orders_kanban_view
)

urlpatterns = [
    path('', orders, name="orders"),
    path('create/', create_order_view, name='create_order'),
    path('<int:pk>/', get_order_view, name='get_order_by_id'),
    path('update/<int:pk>/', edit_order_page, name='edit_order'), 
    path('delete/<int:pk>/', delete_order_view, name='delete_order'),
    path('list/', list_orders_view, name='list_orders'), 
    path('kanban/', orders_kanban_view, name='orders_kanban'),
    path('update_status/', update_order_status, name='update_order_status'),  # Ensure this matches the URL used in the JavaScript fetch request
]