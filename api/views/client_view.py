from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from api.services.client_service import list_clients, get_client_by_id, create_client, update_client, delete_client
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from api.models.client_model import Client

@login_required
def client_edit_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)  # Busca o cliente ou retorna 404
    return render(request, 'main/clients/edit.html', {
        'client': client,
        'isLoggedIn': request.user.is_authenticated,
    })

@login_required
def clients(request):
    clients_list = list_clients()
    return render(request, 'main/clients/all.html', {
        'isLoggedIn': request.user.is_authenticated,
        'clients': clients_list,
    })

@require_http_methods(["GET"])
def list_clients_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    clients_list = list_clients(page, page_size)
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

@login_required
@require_http_methods(["GET", "POST"])
def update_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == "POST":
        try:
            # Captura os dados do formulário e atualiza os campos do cliente
            client.name = request.POST.get('name', client.name)
            client.phone_number = request.POST.get('phoneNumber', client.phone_number)
            client.city = request.POST.get('city', client.city)
            client.address = request.POST.get('address', client.address)
            # Converte 'true' para True e 'false' para False
            client.is_active = request.POST.get('active') == 'true'

            # Salva o cliente atualizado
            client.save()

            # Adiciona uma mensagem de sucesso
            messages.success(request, 'Client updated successfully!')
        except Exception as e:
            # Adiciona uma mensagem de erro em caso de falha
            messages.error(request, f'Failed to update client: {str(e)}')

        # Redireciona para a página de edição
        return HttpResponseRedirect(reverse('client_edit_page', args=[client_id]))

    return render(request, 'main/clients/edit.html', {
        'client': client,
        'isLoggedIn': request.user.is_authenticated,
    })

@require_http_methods(["DELETE"])
def delete_client_view(request, client_id):
    success = delete_client(client_id)
    if success:
        return JsonResponse({"message": "Client deleted successfully"}, status=204)
    return JsonResponse({'error': 'Client not found'}, status=404)
