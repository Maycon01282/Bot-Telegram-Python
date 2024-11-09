from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from api.services.auth_service import authenticate_user

def login_view(request):
    login_error = None  # Variável para a mensagem de erro
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate_user(request, username, password):
                return redirect('orders')  
            else:
                login_error = 'Incorrect username and/or password. Please try again.'  # Defina a mensagem de erro
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
    'form': form,
    'login_error': login_error,
    'isLoggedIn': request.user.is_authenticated,
})
