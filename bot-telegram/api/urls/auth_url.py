from django.urls import path
from api.views.auth_view import login_view
from admin_panel.views import login

urlpatterns = [
    path('', login, name='login'),
    path('login/', login_view, name='login'),
]