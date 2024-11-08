# api/views/order_view.py
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.models.order_model import Order
from api.serializers.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@login_required
def orders(request):
    # Obtenha todas as ordens do banco de dados
    list_orders_view = Order.objects.all()
    # Renderize o template e passe a lista de ordens
    return render(request, 'main/orders/all.html', {
        'orders': list_orders_view,
        'isLoggedIn': request.user.is_authenticated,
    })

@swagger_auto_schema(
    method='get',
    responses={200: OrderSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders_view(request):
    """
    Lista todos os pedidos com paginação.
    """
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    orders = Order.objects.all().order_by('id')
    paginator = Paginator(orders, page_size)
    
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
        
    serializer = OrderSerializer(orders_page, many=True)
    return Response({
        "orders": serializer.data,
        "page": orders_page.number,
        "pages": paginator.num_pages,
        "has_next": orders_page.has_next(),
        "has_previous": orders_page.has_previous(),
    })

@swagger_auto_schema(
    method='get',
    responses={200: OrderSerializer()}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_view(request, pk=None):
    """
    Obtém um pedido pelo seu ID.
    """
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    request_body=OrderSerializer,
    responses={201: OrderSerializer(), 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    """
    Cria um novo pedido.
    """
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    request_body=OrderSerializer,
    responses={200: OrderSerializer(), 400: 'Bad Request'}
)
@swagger_auto_schema(
    method='patch',
    request_body=OrderSerializer,
    responses={200: OrderSerializer(), 400: 'Bad Request'}
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_order_view(request, pk=None):
    """
    Atualiza um pedido existente.
    """
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content'}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order_view(request, pk=None):
    """
    Deleta um pedido pelo ID.
    """
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
