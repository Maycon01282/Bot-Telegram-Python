from django.http import JsonResponse
from api.models.category_model import Category
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def list_categories(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    
    categories = Category.objects.all().order_by('id')  # Add ordering here
    paginator = Paginator(categories, per_page)
    
    try:
        categories_page = paginator.page(page)
    except PageNotAnInteger:
        categories_page = paginator.page(1)
    except EmptyPage:
        categories_page = paginator.page(paginator.num_pages)
    
    categories_data = [{"id": category.id, "name": category.name} for category in categories_page]
    return JsonResponse({
        "categories": categories_data,
        "page": categories_page.number,
        "pages": paginator.num_pages,
        "has_next": categories_page.has_next(),
        "has_previous": categories_page.has_previous(),
    })

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
