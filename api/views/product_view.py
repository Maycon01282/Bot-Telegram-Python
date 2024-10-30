from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from api.models.product_model import Product
from api.services.product_service import list_products, get_product_by_id, create_product, update_product, delete_product
import json

@require_http_methods(["GET"])
def product_list_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    products = list_products(page, page_size)
    return JsonResponse(products, safe=False)

@require_http_methods(["GET"])
def product_detail_view(request, product_id):
    product = get_product_by_id(product_id)
    if product:
        return JsonResponse(product)
    else:
        return HttpResponseNotFound("Product not found")

@require_http_methods(["POST"])
def product_create_view(request):
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