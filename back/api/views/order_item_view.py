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

@require_http_methods(["PUT"])
def update_order_item_view(request, order_item_id):
    data = request.PUT
    order_item = update_order_item(order_item_id, data.get('quantity'))
    return JsonResponse({'id': order_item.id, 'order_id': order_item.order.id, 'item_id': order_item.item.id, 'quantity': order_item.quantity})

@require_http_methods(["DELETE"])
def delete_order_item_view(request, order_item_id):
    delete_order_item(order_item_id)
    return JsonResponse({'status': 'deleted'})

@require_http_methods(["GET"])
def list_order_items_by_order_view(request, order_id):
    order_items = list_order_items_by_order(order_id)
    response_data = [{'id': oi.id, 'order_id': oi.order.id, 'item_id': oi.item.id, 'quantity': oi.quantity} for oi in order_items]
    return JsonResponse(response_data, safe=False)