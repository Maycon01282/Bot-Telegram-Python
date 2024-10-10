from api.models.category_model import Category
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.services.category_service import list_categories, get_category_by_id, create_category, update_category, delete_category
import json

@require_http_methods(["GET"])
def list_categories(request):
    categories = Category.objects.all()
    categories_list = [{"id": category.id, "name": category.name} for category in categories]
    return JsonResponse(categories_list, safe=False)

@require_http_methods(["GET"])
def get_category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        return JsonResponse({"id": category.id, "name": category.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)

@require_http_methods(["POST"])
def create_category(request):
    data = json.loads(request.body)
    category = Category.objects.create(name=data['name'])
    return JsonResponse({"id": category.id, "name": category.name}, status=201)

@require_http_methods(["PUT"])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        data = json.loads(request.body)
        category.name = data.get('name', category.name)
        category.save()
        return JsonResponse({"id": category.id, "name": category.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)

@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"success": True})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)