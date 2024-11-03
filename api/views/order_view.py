from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.services.order_service import list_orders, get_order_by_id, create_order, update_order, delete_order, list_orders_by_client
from api.models.order_model import Order
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    return render(request, 'main/orders/all.html')

@require_http_methods(["GET"])
def list_orders_view(request):
    orders_list = list_orders()
    return JsonResponse(orders_list, safe=False)

@require_http_methods(["GET"])
def get_order_view(request, order_id):
    order_data = get_order_by_id(order_id)
    if order_data:
        return JsonResponse({
            'id': order_data.id,
            'client': order_data.client,
            'status': order_data.status,
            'amount': order_data.amount
        })
    return JsonResponse({'error': 'Order not found'}, status=404)

@require_http_methods(["POST"])
def create_order_view(request):
    data = json.loads(request.body)
    if 'status' in data and data['status'] not in Order.Status.values:
        return JsonResponse({'error': 'Invalid status value'}, status=400)
    order_data = create_order(data['client'], data['status'], data['amount'])
    return JsonResponse({
        'id': order_data.id,
        'client': order_data.client,
        'status': order_data.status,
        'amount': order_data.amount
    }, status=201)

@require_http_methods(["PUT"])
def update_order_view(request, order_id):
    data = json.loads(request.body)
    if 'status' in data and data['status'] not in Order.Status.values:
        return JsonResponse({'error': 'Invalid status value'}, status=400)
    order_data = update_order(order_id, data.get('client'), data.get('status'), data.get('amount'))
    if order_data:
        return JsonResponse({
            'id': order_data.id,
            'client': order_data.client,
            'status': order_data.status,
            'amount': order_data.amount
        })
    return JsonResponse({'error': 'Order not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_order_view(request, order_id):
    success = delete_order(order_id)
    if success:
        return JsonResponse({"message": "Order deleted successfully"}, status=204)
    return JsonResponse({'error': 'Order not found'}, status=404)

@require_http_methods(["GET"])
def list_orders_by_client_view(request):
    client = request.GET.get('client')
    orders_list = list_orders_by_client(client)
    return JsonResponse(orders_list, safe=False)