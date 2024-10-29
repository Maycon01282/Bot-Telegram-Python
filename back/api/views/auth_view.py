from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from api.services.auth_service import authenticate_user

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if authenticate_user(request, username, password):
                return redirect('home')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})