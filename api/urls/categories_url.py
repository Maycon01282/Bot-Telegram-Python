from django.urls import path
from api.views.category_view import (
    list_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    categories,
    create_category_page,
    delete_category_post,
    list_products_by_category_view
)

urlpatterns = [
    path('', categories, name='categories'),
    path('list/', list_categories, name='list_categories'),
    path('<int:category_id>/', get_category_by_id, name='get_category_by_id'),
    path('create/api', create_category, name='create_category_api'),
    path('create/', create_category_page, name='create_category'),
    path('update/<int:category_id>/', update_category, name='update_category'),
    path('delete/<int:category_id>/', delete_category_post, name='delete_category_post'),
    path('<int:category_id>/products/', list_products_by_category_view, name='list_products_by_category')
]
