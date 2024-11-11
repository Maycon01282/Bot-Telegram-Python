from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from api.models.message_model import Message
from api.serializers.serializers import MessageSerializer

@swagger_auto_schema(method='get', responses={200: MessageSerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_messages_view(request):
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

@swagger_auto_schema(method='get', responses={200: MessageSerializer()})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_message_view(request, pk):
    message = get_object_or_404(Message, id=pk)
    serializer = MessageSerializer(message)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=MessageSerializer, responses={201: MessageSerializer()})
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message_view(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=MessageSerializer, responses={200: MessageSerializer()})
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_message_view(request, pk):
    message = get_object_or_404(Message, id=pk)
    serializer = MessageSerializer(message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_message_view(request, pk):
    message = get_object_or_404(Message, id=pk)
    message.delete()
    return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@login_required
def list_messages(request):
    all_messages = Message.objects.all()
    return render(request, 'main/messages/all.html', {
        'all_messages': all_messages
    })

@login_required
def create_message(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            try:
                Message.objects.create(name=title, description=title, text=content)
                messages.success(request, 'Message created successfully!')
                return redirect('messages')
            except IntegrityError:
                errors = {'title': 'A message with this title already exists.'}
                return render(request, 'main/messages/add.html', {
                    'errors': errors,
                    'isLoggedIn': request.user.is_authenticated
                })
        else:
            errors = {}
            if not title:
                errors['title'] = 'Title is required.'
            if not content:
                errors['content'] = 'Content is required.'
            return render(request, 'main/messages/add.html', {
                'errors': errors,
                'isLoggedIn': request.user.is_authenticated
            })

    return render(request, 'main/messages/add.html', {
        'isLoggedIn': request.user.is_authenticated,
        'errors': {}
    })

@login_required
def update_message_page(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.method == 'POST':
        # Atualize o objeto 'message' com os dados do formulário
        serializer = MessageSerializer(message, data=request.POST, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Message updated successfully!')
            return redirect('messages')  # Redirecione para a lista de mensagens
        else:
            # Exiba mensagens de erro específicas, se houver
            return render(request, 'main/messages/edit.html', {
                'message': message,
                'isLoggedIn': request.user.is_authenticated,
                'messageNameError': serializer.errors.get('name'),
                'messageDescriptionError': serializer.errors.get('description'),
                'messageTextError': serializer.errors.get('text'),
            })

    # Renderize o formulário de edição no caso de uma requisição GET
    return render(request, 'main/messages/edit.html', {
        'message': message,
        'isLoggedIn': request.user.is_authenticated
    })