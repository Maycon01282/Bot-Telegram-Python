# admin_panel/context_processors.py

def global_context(request):
    return {
        'isLoggedIn': request.user.is_authenticated,
        'user': request.user,
    }
