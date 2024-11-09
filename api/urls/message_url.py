from django.urls import path
from api.views.message_view import (
    list_messages_view,
    create_message_view,
    get_message_view,
    update_message_view,
    delete_message_view,
)

urlpatterns = [
    path('', list_messages_view, name='message'),
    path('create/', create_message_view, name='create_message'),
    path('<int:message_id>/', get_message_view, name='get_message'),
    path('update/<int:message_id>/', update_message_view, name='update_message'),
    path('delete/<int:message_id>/', delete_message_view, name='delete_message'),
]