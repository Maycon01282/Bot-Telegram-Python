from django.db import IntegrityError
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from api.models import User 
from django.contrib import messages
from api.serializers.serializers import UserSerializer
from api.services.user_service import UserService
from drf_yasg.utils import swagger_auto_schema

@login_required
def users(request):
    users = User.objects.all()
    return render(request, 'main/users/all.html', {'users': users})

    users = User.objects.all()
    return render(request, 'main/users/all.html', {
        'users': users,
        'isLoggedIn': request.user.is_authenticated,
    })
user_service = UserService()
def register(request):
    return render(request, 'register.html')

@swagger_auto_schema(method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
def list_users_view(_):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', responses={200: UserSerializer()})
@api_view(['GET'])
def get_user_view(_, pk=None):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201: UserSerializer()})
@api_view(['POST'])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"email": ["User with this email already exists."]}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=UserSerializer, responses={200: UserSerializer()})
@api_view(['PUT'])
def update_user_view(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
def delete_user_view(_, pk=None):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

def create_user_page(request):
    roles = [
        {'name': 'admin', 'value': 'Admin'},
        {'name': 'editor', 'value': 'Editor'},
        {'name': 'viewer', 'value': 'Viewer'}
    ]
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role_name = request.POST.get('role')
        errors = {}
        if not name:
            errors['name'] = 'Name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'
        if not role_name:
            errors['role'] = 'Role is required.'
        if errors:
            return render(request, 'main/users/add.html', {
                'errors': errors,
                'isLoggedIn': request.user.is_authenticated,
                'roles': roles,
            })
        try:
            user = User.objects.create_user(email=email, name=name, password=password)
            user.role = role_name
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('users')
        except IntegrityError:
            errors['email'] = 'A user with this email already exists.'
        except Exception as e:
            errors['general'] = f'Unexpected error: {str(e)}'
        return render(request, 'main/users/add.html', {
            'errors': errors,
            'isLoggedIn': request.user.is_authenticated,
            'roles': roles,
        })
    return render(request, 'main/users/add.html', {
        'isLoggedIn': request.user.is_authenticated,
        'errors': {},
        'roles': roles,
    })
    
@login_required
def update_user_page(request, pk):
    user = get_object_or_404(User, pk=pk)
    roles = [{'name': 'admin', 'value': 'Admin'}, {'name': 'editor', 'value': 'Editor'}, {'name': 'viewer', 'value': 'Viewer'}]

    if request.method == 'POST':
        data = request.POST.copy()
        errors = {}

        # Validations
        if not data.get('name'):
            errors['name'] = 'Name is required.'
        if not data.get('username'):
            errors['username'] = 'Username is required.'
        if not data.get('role'):
            errors['role'] = 'Role is required.'

        if errors:
            return render(request, 'main/users/edit.html', {'errors': errors, 'roles': roles, 'user': user})

        try:
            user.name = data['name']
            user.username = data['username']
            if data.get('password'):
                user.set_password(data['password'])
            user.role = data['role']
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('users')
        except IntegrityError:
            errors['username'] = 'A user with this username already exists.'
            return render(request, 'main/users/edit.html', {'errors': errors, 'roles': roles, 'user': user})

    return render(request, 'main/users/edit.html', {'user': user, 'roles': roles})
    user = get_object_or_404(User, pk=pk)
    roles = [
            {'name': 'admin', 'value': 'Admin'},
            {'name': 'editor', 'value': 'Editor'},
            {'name': 'viewer', 'value': 'Viewer'}
        ]
    if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role_name = request.POST.get('role')
            errors = {}
            if not name:
                errors['name'] = 'Name is required.'
            if not email:
                errors['email'] = 'Email is required.'
            if not role_name:
                errors['role'] = 'Role is required.'
            if errors:
                return render(request, 'main/users/edit.html', {
                    'errors': errors,
                    'isLoggedIn': request.user.is_authenticated,
                    'roles': roles,
                    'user': user,
                })
            try:
                user.name = name
                user.email = email
                if password:
                    user.set_password(password)
                user.role = role_name
                user.save()
                messages.success(request, 'User updated successfully!')
                return redirect('users')
            except IntegrityError:
                errors['email'] = 'A user with this email already exists.'
            except Exception as e:
                errors['general'] = f'Unexpected error: {str(e)}'
            return render(request, 'main/users/edit.html', {
                'errors': errors,
                'isLoggedIn': request.user.is_authenticated,
                'roles': roles,
                'user': user,
            })
            return render(request, 'main/users/edit.html', {
            'isLoggedIn': request.user.is_authenticated,
            'errors': {},
            'roles': roles,
            'user': user,
        })
        
def delete_user(request, pk=None):
    user = get_object_or_404(User, pk=pk)
    try:
        user.delete()
        messages.success(request, "User deleted successfully")
    except Exception as e:
        messages.error(request, f"Error deleting user: {e}")
    return redirect('users') 