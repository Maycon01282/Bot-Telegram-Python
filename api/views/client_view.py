from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from api.services.client_service import list_clients, get_client_by_id, create_client, update_client, delete_client
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def clients(request):
    return render(request, 'clients.html')

@require_http_methods(["GET"])
def list_clients_view(request):
    clients_list = list_clients()
    return JsonResponse(clients_list, safe=False)

@require_http_methods(["GET"])
def get_client_view(request, client_id):
    client_data = get_client_by_id(client_id)
    if client_data:
        return JsonResponse(client_data)
    return JsonResponse({'error': 'Client not found'}, status=404)

@require_http_methods(["POST"])
def create_client_view(request):
    data = json.loads(request.body)
    client_data = create_client(data)
    return JsonResponse(client_data, status=201)

@require_http_methods(["PUT"])
def update_client_view(request, client_id):
    data = json.loads(request.body)
    client_data = update_client(client_id, data)
    if client_data:
        return JsonResponse(client_data)
    return JsonResponse({'error': 'Client not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_client_view(request, client_id):
    success = delete_client(client_id)
    if success:
        return JsonResponse({"message": "Client deleted successfully"}, status=204)
    return JsonResponse({'error': 'Client not found'}, status=404)
