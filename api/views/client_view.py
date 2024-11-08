from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from api.models.client_model import Client
from api.serializers.serializers import ClientSerializer

@swagger_auto_schema(method='get', responses={200: ClientSerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_clients_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    clients = Client.objects.all().order_by('id')
    paginator = Paginator(clients, page_size)
    try:
        clients_page = paginator.page(page)
    except PageNotAnInteger:
        clients_page = paginator.page(1)
    except EmptyPage:
        clients_page = paginator.page(paginator.num_pages)
    serializer = ClientSerializer(clients_page, many=True)
    return Response({
        "clients": serializer.data,
        "page": clients_page.number,
        "pages": paginator.num_pages,
        "has_next": clients_page.has_next(),
        "has_previous": clients_page.has_previous(),
    })
    
@login_required
def client_edit_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)  # Busca o cliente ou retorna 404
    return render(request, 'main/clients/edit.html', {
        'client': client,
        'isLoggedIn': request.user.is_authenticated,
    })

@login_required
def clients(request):
    clients_list = list_clients_view()
    return render(request, 'main/clients/all.html', {
        'isLoggedIn': request.user.is_authenticated,
        'clients': clients_list,
    })

@swagger_auto_schema(method='get', responses={200: ClientSerializer()})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    serializer = ClientSerializer(client)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=ClientSerializer, responses={201: ClientSerializer()})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_client_view(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=ClientSerializer, responses={200: ClientSerializer()})
@api_view(['PUT'])
@permission_classes([permissions.AllowAny])
def update_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def delete_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    client.delete()
    return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
