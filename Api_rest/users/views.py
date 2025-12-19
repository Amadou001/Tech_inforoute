from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


API_BASE_URL = "http://127.0.0.1:8000/api/users" 

username = openapi.Parameter(
    'username', openapi.IN_PATH, description="the username", type=openapi.TYPE_STRING, required=True
)
password = openapi.Parameter(
    'password', openapi.IN_PATH, description="the password", type=openapi.TYPE_STRING, required=True
)
email = openapi.Parameter(
    'email', openapi.IN_PATH, description="the email", type=openapi.TYPE_STRING, required=True
)
@swagger_auto_schema(
    method='post',
    manual_parameters=[username, email, password],
    request_body=RegisterSerializer,
    responses={201: UserSerializer, 400: 'Validation error'},
    operation_description="Register a new user and generate an authentication token automatically."
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and create an auth token automatically.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



username = openapi.Parameter(
    'username', openapi.IN_PATH, description="the username", type=openapi.TYPE_STRING, required=True
)
password = openapi.Parameter(
    'password', openapi.IN_PATH, description="the password", type=openapi.TYPE_STRING, required=True
)
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    }
)

@swagger_auto_schema(
    method='post',
    request_body=login_request_body,
    manual_parameters=[username, password],
    responses={200: UserSerializer, 401: 'Invalid credentials'},
    operation_description="Authenticate existing user and return their token."
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate existing user and return their token.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "user": UserSerializer(user).data,
        "token": token.key
    }, status=status.HTTP_200_OK)




username = openapi.Parameter(
    'username', openapi.IN_PATH, description="the username", type=openapi.TYPE_STRING, required=True
)

delete_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username to delete')
    }
)

@swagger_auto_schema(
    method='post',
    manual_parameters=[username],
    responses={200: 'User deleted successfully', 404: 'User not found'},
    operation_description="Delete an existing user by username."
)
@permission_classes([AllowAny])
@api_view(['POST'])
def delete_user(request):
    """
    Delete an existing user by username.
    """
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



username = openapi.Parameter(
    'username', openapi.IN_PATH, description="the username", type=openapi.TYPE_STRING, required=True
)
logout_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username to logout')
    }
)

@swagger_auto_schema(
    method='post',
    request_body=logout_request_body,
    manual_parameters=[username],
    responses={200: 'User logged out successfully', 404: 'User or token not found'},
    operation_description="Logout a user by deleting their auth token."
)
@permission_classes([AllowAny])
@api_view(['POST'])
def logout_user(request):
    """
    Logout user by deleting their auth token.
    """
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        token = Token.objects.get(user=user)
        token.delete()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Token.DoesNotExist:
        return Response({"error": "Token not found: this user is not logged in"}, status=status.HTTP_404_NOT_FOUND)
    



def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = requests.post(f"{API_BASE_URL}/register/", json={
            "username": username,
            "email": email,
            "password": password
        })

        if response.status_code == 201:
            return HttpResponse(f"{response.json()}")
        else:
            return HttpResponse(f"Error: {response.json()}")
    return render(request, 'users/register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        response = requests.post(f"{API_BASE_URL}/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            return HttpResponse(f"{data}")
        else:
            return HttpResponse(f"Error: {response.json()}")
    return render(request, 'users/login.html')


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

