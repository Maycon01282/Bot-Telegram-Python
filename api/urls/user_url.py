from django.urls import path
from api.views.user_view import (
    create_user_view,
    update_user_view,
    delete_user_view,
    get_user_view,
    list_users_view,
    register,
    users
)

urlpatterns = [
    path('', users, name='users'),
    path("register/", register, name='register'),
    path('list/', list_users_view, name='list_users'),
    path('<int:user_id>/', get_user_view, name='get_user'),
    path('create/', create_user_view, name='create_user'),
    path('update/<int:user_id>/', update_user_view, name='update_user'),
    path('delete/<int:user_id>/', delete_user_view, name='delete_user'),
]