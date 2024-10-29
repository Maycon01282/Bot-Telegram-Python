from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from api.services.user_service import UserService
import json

user_service = UserService()

@require_http_methods(["GET"])
def user_list_view(request):
    users_list = user_service.list_users()
    return JsonResponse(users_list, safe=False)

@require_http_methods(["GET"])
def user_detail_view(request, user_id=None, email=None):
    if user_id:
        user_data = user_service.get_user_by_id(user_id)
        if user_data:
            return JsonResponse(user_data)
        else:
            return HttpResponseNotFound("User not found")
    elif email:
        user_data = user_service.get_user_by_email(email)
        if user_data:
            return JsonResponse(user_data)
        else:
            return HttpResponseNotFound("User not found")
    else:
        return HttpResponseBadRequest("User ID or email required")

@require_http_methods(["POST"])
def user_create_view(request):
    try:
        data = json.loads(request.body)
        user_data = user_service.create_user(data)
        return JsonResponse(user_data, status=201)
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")

@require_http_methods(["PUT"])
def user_update_view(request, user_id):
    try:
        data = json.loads(request.body)
        user_data = user_service.update_user(user_id, data)
        if user_data:
            return JsonResponse(user_data)
        else:
            return HttpResponseNotFound("User not found")
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid data")

@require_http_methods(["DELETE"])
def user_delete_view(request, user_id):
    success = user_service.delete_user(user_id)
    if success:
        return JsonResponse({"message": "User deleted successfully"})
    else:
        return HttpResponseNotFound("User not found")
