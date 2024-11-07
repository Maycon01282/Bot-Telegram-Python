# api/views/order_item_view.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.models.order_item_model import OrderItem
from api.serializers.serializers import OrderItemSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    ##permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        order_item = get_object_or_404(OrderItem, pk=pk)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        order_item = get_object_or_404(OrderItem, pk=pk)
        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order_item = get_object_or_404(OrderItem, pk=pk)
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list_order_items(self, request, order_id=None):
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