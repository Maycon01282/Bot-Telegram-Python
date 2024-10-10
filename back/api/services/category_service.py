from api.models.category_model import Category
from django.core.exceptions import ObjectDoesNotExist

def list_categories():
    categories = Category.objects.all()
    return [{"id": category.id, "name": category.name} for category in categories]

def get_category_by_id(category_id):
    try:
        category = Category.objects.get(id=category_id)
        return {"id": category.id, "name": category.name}
    except ObjectDoesNotExist:
        return None

def create_category(data):
    category = Category.objects.create(
        name=data['name']
    )
    return {"id": category.id, "name": category.name}

def update_category(category_id, data):
    try:
        category = Category.objects.get(id=category_id)
        category.name = data.get('name', category.name)
        category.save()
        return {"id": category.id, "name": category.name}
    except ObjectDoesNotExist:
        return None

def delete_category(category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return True
    except ObjectDoesNotExist:
        return False
