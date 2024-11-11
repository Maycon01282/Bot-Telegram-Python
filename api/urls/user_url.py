from django.urls import path
from api.views.user_view import (
    create_user_view,
    update_user_view,
    delete_user_view,
    get_user_view,
    list_users_view,
    register,
    users,
    create_user_page,
    update_user_page
)

urlpatterns = [
    path('', users, name='users'),
    path('register/', register, name='register'),
    path('list/', list_users_view, name='list_users'),
    path('<int:user_id>/', get_user_view, name='get_user'),
    path('create/api', create_user_view, name='create_user_api'),
    path('create/', create_user_page, name='create_user_page'),
    path('update/<int:pk>/api', update_user_view, name='update_user'),
    path('update/<int:pk>/', update_user_page, name='update_user_page'),
    path('delete/<int:pk>/', delete_user_view, name='delete_user'),
]