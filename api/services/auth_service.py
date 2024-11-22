
from django.contrib.auth import authenticate, login

def authenticate_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False
