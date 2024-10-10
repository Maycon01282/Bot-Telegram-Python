from django.urls import path
from api.views.category_view import list_categories, get_category_by_id, create_category, update_category, delete_category

urlpatterns = [
    path('categories/', list_categories, name='list_categories'),
    path('categories/<int:category_id>/', get_category_by_id, name='get_category_by_id'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/update/<int:category_id>/', update_category, name='update_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
]