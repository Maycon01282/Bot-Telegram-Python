# api/views/user_view.py
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from api.models import User  # Importa o modelo de usuário customizado
from api.serializers.serializers import UserSerializer
from api.services.user_service import UserService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@login_required
def users(request):
    user_service = UserService()
    users_list = user_service.list_users()
    return render(request, 'main/users/all.html', {
        'users': users_list,
        'isLoggedIn': request.user.is_authenticated,
    })

user_service = UserService()

def register(request):
    return render(request, 'register.html')

@swagger_auto_schema(method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users_view(request):
    """
    Lista todos os usuários.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', responses={200: UserSerializer()})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_view(request, pk=None):
    """
    Obtém um usuário pelo seu ID.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer(), 400: 'Bad Request'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_view(request):
    """
    Cria um novo usuário.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['put', 'patch'], request_body=UserSerializer, responses={200: UserSerializer(), 400: 'Bad Request'})
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_view(request, pk=None):
    """
    Atualiza um usuário existente.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_view(request, pk=None):
    """
    Deleta um usuário pelo ID.
    """
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
