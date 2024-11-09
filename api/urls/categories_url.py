from django.urls import path
from api.views.category_view import (
    list_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    categories
)

urlpatterns = [
    path('', categories, name='categories'),  # URL for categories
    path('list/', list_categories, name='list_categories'),  # URL to list categories
    path('<int:category_id>/', get_category_by_id, name='get_category_by_id'),  # URL to get category by ID
    path('create/', create_category, name='create_category'),  # URL to create new category
    path('update/<int:category_id>/', update_category, name='update_category'),  # URL to update category
    path('delete/<int:category_id>/', delete_category, name='delete_category'),  # URL to delete category
]
