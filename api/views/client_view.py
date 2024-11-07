# api/views/client_view.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.models.client_model import Client
from api.serializers.serializers import ClientSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    ##permission_classes = [IsAuthenticated]

    def list_clients(self, request):
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

    def get_client_by_id(self, request, pk=None):
        client = get_object_or_404(Client, id=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def create_client(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_client(self, request, pk=None):
        client = get_object_or_404(Client, id=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_client(self, request, pk=None):
        client = get_object_or_404(Client, id=pk)
        client.delete()
        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)