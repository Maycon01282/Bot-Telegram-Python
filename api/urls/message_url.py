from django.urls import path
from api.views.message_view import (
    list_messages_view,
    create_message_view,
    get_message_view,
    update_message_view,
    delete_message_view,
    list_messages,
    create_message,
    update_message_page,
)

urlpatterns = [
    path('', list_messages, name='messages'),
    path('list/', list_messages_view, name='message_list'),
    path('create/', create_message, name='create_message'),
    path('create/api', create_message_view, name='create_message_api'),   
    path('<int:pk>/', get_message_view, name='get_message'),
    path('update/<int:pk>/api', update_message_view, name='update_message_api'),
    path('update/<int:pk>/', update_message_page, name='update_message'),
    path('delete/<int:pk>/', delete_message_view, name='delete_message'),
]