from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.models.user_model import User
from api.services.user_service import UserService
from api.models.category_model import Category  # Add this import

@login_required
def categories(request):
    user_service = UserService()
    categories_list = Category.objects.all()
    user_data = user_service.get_user_by_id(request.user.id)
    return render(request, 'main/categories/all.html', {
        'categories': categories_list,
        'isLoggedIn': request.user.is_authenticated,
    })

@require_http_methods(["GET"])
def list_categories(request):
    categories = Category.objects.all()
    categories_data = [{"id": category.id, "name": category.name} for category in categories]
    return JsonResponse(categories_data, safe=False)

@require_http_methods(["GET"])
def get_category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        return JsonResponse({"id": category.id, "name": category.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def create_category(request):
    try:
        data = json.loads(request.body)
        category = Category.objects.create(name=data['name'])
        return JsonResponse({"id": category.id, "name": category.name}, status=201)
    except KeyError:
        return JsonResponse({"error": "Invalid data."}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        data = json.loads(request.body)
        category.name = data.get('name', category.name)
        category.save()
        return JsonResponse({"id": category.id, "name": category.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)
    except KeyError:
        return JsonResponse({"error": "Invalid data."}, status=400)

@require_http_methods(["GET"])
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
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"message": "Category deleted."}, status=204)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)