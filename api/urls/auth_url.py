from django.urls import path
from django.contrib.auth.views import LogoutView
from api.views.auth_view import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # URL para o logout
]