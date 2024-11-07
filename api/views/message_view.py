# api/views/message_view.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.models.message_model import Message
from api.serializers.serializers import MessageSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    ##permission_classes = [IsAuthenticated]

    def list_messages(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        messages = Message.objects.all().order_by('id')
        paginator = Paginator(messages, page_size)
        try:
            messages_page = paginator.page(page)
        except PageNotAnInteger:
            messages_page = paginator.page(1)
        except EmptyPage:
            messages_page = paginator.page(paginator.num_pages)
        serializer = MessageSerializer(messages_page, many=True)
        return Response({
            "messages": serializer.data,
            "page": messages_page.number,
            "pages": paginator.num_pages,
            "has_next": messages_page.has_next(),
            "has_previous": messages_page.has_previous(),
        })

    def get_message_by_id(self, request, pk=None):
        message = get_object_or_404(Message, id=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def create_message(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_message(self, request, pk=None):
        message = get_object_or_404(Message, id=pk)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_message(self, request, pk=None):
        message = get_object_or_404(Message, id=pk)
        message.delete()
        return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)