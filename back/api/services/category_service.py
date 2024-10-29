from django.http import JsonResponse
from api.models.category_model import Category
from django.core.exceptions import ObjectDoesNotExist

def list_categories(request):
    categories = Category.objects.all()
    categories_data = [{"id": category.id, "name": category.name} for category in categories]
    return JsonResponse(categories_data, safe=False)

def get_category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        return JsonResponse({"id": category.id, "name": category.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)

def create_category(request):
    if request.method == 'POST':
        data = request.POST  # Use request.body para JSON
        category = Category.objects.create(name=data['name'])
        return JsonResponse({"id": category.id, "name": category.name}, status=201)
    return JsonResponse({"error": "Invalid method."}, status=405)

def update_category(request, category_id):
    if request.method == 'PUT':
        try:
            category = Category.objects.get(id=category_id)
            data = request.PUT  # Use request.body para JSON
            category.name = data.get('name', category.name)
            category.save()
            return JsonResponse({"id": category.id, "name": category.name})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found."}, status=404)
    return JsonResponse({"error": "Invalid method."}, status=405)

def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"message": "Category deleted."}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found."}, status=404)
    return JsonResponse({"error": "Invalid method."}, status=405)
