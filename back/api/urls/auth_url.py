from django.urls import path
from api.views.auth_view import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
]