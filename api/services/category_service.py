from django.http import JsonResponse
from api.models.category_model import Category
from api.serializers import CategorySerializer
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def list_categories(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    
    categories = Category.objects.all().order_by('id')
    paginator = Paginator(categories, per_page)
    
    try:
        categories_page = paginator.page(page)
    except PageNotAnInteger:
        categories_page = paginator.page(1)
    except EmptyPage:
        categories_page = paginator.page(paginator.num_pages)
    
    serializer = CategorySerializer(categories_page, many=True)
    return JsonResponse({
        "categories": serializer.data,
        "page": categories_page.number,
        "pages": paginator.num_pages,
        "has_next": categories_page.has_next(),
        "has_previous": categories_page.has_previous(),
    })

@csrf_exempt
def get_category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)

@csrf_exempt
def create_category(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({"error": "Invalid method."}, status=405)

@csrf_exempt
def update_category(request, category_id):
    if request.method == 'PUT':
        try:
            category = Category.objects.get(id=category_id)
            data = JSONParser().parse(request)
            serializer = CategorySerializer(category, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found."}, status=404)
    return JsonResponse({"error": "Invalid method."}, status=405)

@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"message": "Category deleted."}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found."}, status=404)
    return JsonResponse({"error": "Invalid method."}, status=405)
