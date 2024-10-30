from django.urls import path
from api.views.user_view import (
    create_user_view,
    update_user_view,
    delete_user_view,
    get_user_view,
    list_users_view
)
from admin_panel.views import (users)

urlpatterns = [
    path('', users, name='users'),
    path('users/', list_users_view, name='list_users'),
    path('users/<int:user_id>/', get_user_view, name='get_user'),
    path('users/create/', create_user_view, name='create_user'),
    path('users/<int:user_id>/update/', update_user_view, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user_view, name='delete_user'),
]