from django.urls import path 
from api.views.home_view import home

urlpatterns = [
    path('', home, name='home'),
]