from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models.order_model import Order

@login_required
def home(request):
    list_orders_view = Order.objects.all()
    return render(request, 'main/orders/all.html', {
        'orders':  list_orders_view,
        'isLoggedIn': request.user.is_authenticated,
    })