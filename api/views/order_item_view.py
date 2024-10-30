from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.services.order_item_service import (
    create_order_item,
    get_order_item_by_id,
    update_order_item,
    delete_order_item,
    list_order_items_by_order
)
import json

@require_http_methods(["POST"])
def create_order_item_view(request):
    data = request.POST
    order_item = create_order_item(data['order_id'], data['item_id'], data['quantity'])
    return JsonResponse({'id': order_item.id, 'order_id': order_item.order.id, 'item_id': order_item.item.id, 'quantity': order_item.quantity})

@require_http_methods(["GET"])
def get_order_item_view(request, order_item_id):
    order_item = get_order_item_by_id(order_item_id)
    return JsonResponse({'id': order_item.id, 'order_id': order_item.order.id, 'item_id': order_item.item.id, 'quantity': order_item.quantity})

@require_http_methods(["GET"])
def list_order_items_view(request, order_id):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    order_items_data = list_order_items_by_order(order_id, page, page_size)
    return JsonResponse(order_items_data, safe=False)

@require_http_methods(["PUT"])
def update_order_item_view(request, order_item_id):
    data = json.loads(request.body)
    quantity = data.get('quantity')
    order_item = update_order_item(order_item_id, quantity)
    return JsonResponse({'id': order_item.id, 'order_id': order_item.order.id, 'item_id': order_item.item.id, 'quantity': order_item.quantity})

@require_http_methods(["DELETE"])
def delete_order_item_view(request, order_item_id):
    delete_order_item(order_item_id)
    return JsonResponse({'message': 'Order item deleted successfully'})