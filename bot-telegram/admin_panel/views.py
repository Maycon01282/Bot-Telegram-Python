from django.shortcuts import render

def login(request):
    return render(request, 'login.html')
def home(request):
    return render(request, 'home.html')
def orders(request):
    return render(request, 'orders.html')
def clients(request):
    return render(request, 'clients.html')
def users(request):
    return render(request, 'users.html')
def products(request):
    return render(request, 'products.html')
def category(request):
    return render(request, 'category.html')