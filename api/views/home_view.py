from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'main/orders/all.html', {
        'isLoggedIn': request.user.is_authenticated,
    })
