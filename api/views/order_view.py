from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.services.order_service import list_orders, get_order_by_id, create_order, update_order, delete_order
from api.models.order_model import Order
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    # Obtenha todas as ordens do banco de dados
    orders_list = Order.objects.all()
    
    # Renderize o template e passe a lista de ordens
    return render(request, 'main/orders/all.html', {
        'orders': orders_list,
        'isLoggedIn': request.user.is_authenticated,
    })

@require_http_methods(["GET"])
def list_orders_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    orders_list = list_orders(page, page_size)
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