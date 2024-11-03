from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from api.services.user_service import UserService
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def users(request):
    return render(request, 'users.html')

user_service = UserService()

def register(request):
    return render(request, 'register.html')

@require_http_methods(["POST"])
def create_user_view(request):
    data = json.loads(request.body)
    user_data = user_service.create_user(data)
    return JsonResponse(user_data, status=201)

@require_http_methods(["PUT"])
def update_user_view(request, user_id):
    data = json.loads(request.body)
    user_data = user_service.update_user(user_id, data)
    if user_data:
        return JsonResponse(user_data)
    return JsonResponse({'error': 'User not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_user_view(request, user_id):
    success = user_service.delete_user(user_id)
    if success:
        return JsonResponse({"message": "User deleted successfully"}, status=204)
    return JsonResponse({'error': 'User not found'}, status=404)

@require_http_methods(["GET"])
def get_user_view(request, user_id):
    user_data = user_service.get_user_by_id(user_id)
    if user_data:
        return JsonResponse(user_data)
    return JsonResponse({'error': 'User not found'}, status=404)

@require_http_methods(["GET"])
def list_users_view(request):
    users_list = user_service.list_users()
    return JsonResponse(users_list, safe=False)