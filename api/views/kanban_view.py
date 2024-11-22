from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from api.models import Order
import json

@require_POST
@csrf_exempt
def update_order_status(request):
    data = json.loads(request.body)
    order_id = data.get('id')
    new_status = data.get('status')

    try:
        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return JsonResponse({'success': True})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)
