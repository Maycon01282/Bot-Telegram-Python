from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.models.order_item_model import OrderItem
from api.serializers.serializers import OrderItemSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(method='get', manual_parameters=[openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER), openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER)], responses={200: OrderItemSerializer(many=True)})
@api_view(['GET'])
def list_order_items_view(request, order_id=None):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    order_items = OrderItem.objects.filter(order_id=order_id).order_by('id')
    paginator = Paginator(order_items, page_size)
    try:
        order_items_page = paginator.page(page)
    except PageNotAnInteger:
        order_items_page = paginator.page(1)
    except EmptyPage:
        order_items_page = paginator.page(paginator.num_pages)   
    serializer = OrderItemSerializer(order_items_page, many=True)
    return Response({
        "order_items": serializer.data,
        "page": order_items_page.number,
        "pages": paginator.num_pages,
        "has_next": order_items_page.has_next(),
        "has_previous": order_items_page.has_previous(),
    })

@swagger_auto_schema(method='get', responses={200: OrderItemSerializer()})
@api_view(['GET'])
def get_order_item_view(request, pk=None):
    order_item = get_object_or_404(OrderItem, pk=pk)
    serializer = OrderItemSerializer(order_item)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=OrderItemSerializer, responses={201: OrderItemSerializer(), 400: 'Bad Request'})
@api_view(['POST'])
def create_order_item_view(request):
    serializer = OrderItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=OrderItemSerializer, responses={200: OrderItemSerializer(), 400: 'Bad Request'})
@swagger_auto_schema(method='patch', request_body=OrderItemSerializer, responses={200: OrderItemSerializer(), 400: 'Bad Request'})
@api_view(['PUT', 'PATCH'])
def update_order_item_view(request, pk=None):
    order_item = get_object_or_404(OrderItem, pk=pk)
    serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
def delete_order_item_view(request, pk=None):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_item.delete()
    return Response({"message": "Order item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
