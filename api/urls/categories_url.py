from django.urls import path, include
from api.views.category_view import list_categories, get_category_by_id, create_category, update_category, delete_category

urlpatterns = [
    path('list/', list_categories, name='list_categories'),  # URL para listar categorias
    path('<int:category_id>/', get_category_by_id, name='get_category_by_id'),  # URL para obter categoria por ID
    path('create/', create_category, name='create_category'),  # URL para criar nova categoria
    path('update/<int:category_id>/', update_category, name='update_category'),  # URL para atualizar categoria
    path('delete/<int:category_id>/', delete_category, name='delete_category'),  # URL para deletar categoria
]
