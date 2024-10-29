from django.urls import path
from api.views.user_view import (
    user_list_view,
    user_detail_view,
    user_create_view,
    user_update_view,
    user_delete_view
)

urlpatterns = [
    path('users/', user_list_view, name='user_list'),
    path('users/<int:user_id>/', user_detail_view, name='user_detail_by_id'),
    path('users/email/<str:email>/', user_detail_view, name='user_detail_by_email'),
    path('users/create/', user_create_view, name='user_create'),
    path('users/update/<int:user_id>/', user_update_view, name='user_update'),
    path('users/delete/<int:user_id>/', user_delete_view, name='user_delete'),
]