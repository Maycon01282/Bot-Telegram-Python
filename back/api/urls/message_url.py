from django.urls import path
from api.views import create_message_view, get_message_view, update_message_view, delete_message_view

urlpatterns = [
    path('message/', create_message_view, name='create_message'),
    path('message/<int:message_id>/', get_message_view, name='get_message'),
    path('message/<int:message_id>/', update_message_view, name='update_message'),
    path('message/<int:message_id>/', delete_message_view, name='delete_message'),
]