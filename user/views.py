from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.serializers import UserSerializer, UserRequestSerializer
from django.contrib.auth.models import User

from utils import paginations
from utils.response_api_serializer import ResponseAPISerializer

@extend_schema(
    description='Get all users',
    tags=['user'],
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Page size'),
    ],
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['GET'])
@csrf_exempt
def get_users(request):
    paginator = paginations.CustomPagination()
    
    users = User.objects.all().order_by('id')
    result_page = paginator.paginate_queryset(users, request)
    user_serializer = UserSerializer(result_page, many=True)

    return Response({
        'message': 'get user success',
        'data': paginator.get_paginated_response(user_serializer.data),
        'errors': None
    })

@extend_schema(
    description='Get user by id',
    tags=['user'],
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['GET'])
@csrf_exempt
def get_user_by_id(request, id):
    user = None
    try: 
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({
            'message': 'user not found',
            'data': None,
            'errors': None
        }, status=status.HTTP_404_NOT_FOUND)
    
    user_serializer = UserSerializer(user)
    return Response({
        'message': 'get user success',
        'data': user_serializer.data,
        'errors': None
    })


@extend_schema(
    description='Create user',
    tags=['user'],
    request=UserRequestSerializer,
    responses={
        201: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['POST'])
@csrf_exempt
def add_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = User.objects.create_user(
            username=user_serializer.data['username'],
            email=user_serializer.data['email'],
        )

        user.set_password(request.data['password'])
        user.save()

        return Response({
            'message': 'user create success',
            'data': {
                'id': user.pk,
            },
            'errors': None
        }, status=status.HTTP_201_CREATED)

    return Response({
        'message': 'user create failed!',
        'data': None,
        'errors': user_serializer.errors
    })


@extend_schema(
    description='Update user',
    tags=['user'],
    request=UserRequestSerializer,
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['PUT'])
@csrf_exempt
def update_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = User.objects.get(id=request.data['id'])
        user.username = user_serializer.data['username']
        user.email = user_serializer.data['email']
        user.first_name = user_serializer.data['first_name']
        user.last_name = user_serializer.data['last_name']
        
        if 'password' in request.data:
            user.set_password(request.data['password'])
            
        user.save()
    
        return Response({
            'message': 'user update success',
            'data': user_serializer.data,
            'errors': None
        })
    
    return Response({
        'message': 'api user update',
        'data': None,
        'errors': user_serializer.errors
    })


@extend_schema(
    description='Delete user',
    tags=['user'],
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['DELETE'])
@csrf_exempt
def delete_user(request, id):
    user = None
    try: 
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({
            'message': 'user not found',
            'data': None,
            'errors': None
        }, status=status.HTTP_404_NOT_FOUND)
    
    user.delete()

    return Response({
        'message': 'delete user success',
        'data': None,
        'errors': None
    })