from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api.models.order_model import Order

@login_required
def home(request):
    orders_list = Order.objects.all()
    return render(request, 'main/orders/all.html', {
        'orders': orders_list,
        'isLoggedIn': request.user.is_authenticated,
    })