from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json

from api.services.product_service import (
    list_products, 
    get_product_by_id, 
    create_product, 
    update_product, 
    delete_product
)
from api.models.product_model import Product
from api.models.category_model import Category

@login_required
def products(request):
    products_list = Product.objects.all()
    return render(request, 'main/products/all.html', {
        'products': products_list  
    })

@require_http_methods(["GET"])
def product_list_view(request):
<<<<<<< HEAD
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    products = list_products(page, page_size)
    return JsonResponse(products, safe=False)
=======
    products = Product.objects.all()
    products_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": {
                "id": product.category.id,
                "name": product.category.name
            } if product.category else None,
            "photo_url": product.photo_url 
        }
        for product in products
    ]

    return JsonResponse(products_data, safe=False)
>>>>>>> develop

@require_http_methods(["GET"])
def product_detail_view(request, product_id):
    product = get_product_by_id(product_id)
    if product:
        return JsonResponse(product)
    else:
        return HttpResponseNotFound("Product not found")

@login_required
@require_http_methods(["GET", "POST"])
def product_create_view(request):
<<<<<<< HEAD
    try:
        data = json.loads(request.body)
        product = create_product(data)
        return JsonResponse({
            'id': product.id,
            'category': product.category,
            'photo_url': product.photo_url,
            'name': product.name,
            'description': product.description,
            'price': product.price
        }, status=201)
    except KeyError as e:
        return HttpResponseBadRequest(f"Missing field: {e}")
=======
    categories = Category.objects.all()
    
    if not categories.exists() and request.method == "GET":
        return render(request, 'main/products/add.html', {
            'categories': categories,
            'category_error': "No categories available. Please add a category first."
        })

    if request.method == "POST":
        try:
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)

            data = {
                'category': category,
                'photo_url': request.FILES.get('photo') or request.POST.get('photo_url'),
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'price': float(request.POST.get('price')),
            }

            product = create_product(data)

            return redirect('products')

        except Category.DoesNotExist:
            return HttpResponseBadRequest("Invalid category")
        except KeyError:
            return HttpResponseBadRequest("Missing required data")

    return render(request, 'main/products/add.html', {'categories': categories})
>>>>>>> develop

@require_http_methods(["PUT"])
def product_update_view(request, product_id):
    try:
        data = json.loads(request.body)
        product = update_product(product_id, data)
        if product:
            return JsonResponse(product)
        else:
            return HttpResponseNotFound("Product not found")
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")

@require_http_methods(["DELETE"])
def product_delete_view(request, product_id):
    success = delete_product(product_id)
    if success:
        return JsonResponse({"message": "Product deleted successfully"})
    else:
        return HttpResponseNotFound("Product not found")
