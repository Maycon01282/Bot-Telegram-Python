# api/urls/category_urls.py
from django.urls import path
from api.views.category_view import Category, list_categories, get_category_by_id, create_category, update_category, delete_category

urlpatterns = [
    path('', Category, name='category'),  # Página principal de categorias
    path('list/', list_categories, name='list_categories'),  # URL para listar categorias
    path('<int:category_id>/', get_category_by_id, name='get_category_by_id'),
    path('create/', create_category, name='create_category'),
    path('update/<int:category_id>/', update_category, name='update_category'),
    path('delete/<int:category_id>/', delete_category, name='delete_category'),
]