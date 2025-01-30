from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from utils import paginations
from utils.response_api_serializer import ResponseAPISerializer

from contact.models import Contact
from contact.serializers import ContactSerializer, ContactRequestSerializer

import logging
logger = logging.Logger(__name__)


@extend_schema(
    description='Get all contacts',
    tags=['contact'],
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
def get_contacts(request):
    paginator = paginations.CustomPagination()

    contacts = Contact.objects.all()
    result_page = paginator.paginate_queryset(contacts, request)
    contacts_serializer = ContactSerializer(result_page, many=True)
    return Response({
        'message': 'get contact success',
        'data': paginator.get_paginated_response(contacts_serializer.data),
    })


@extend_schema(
    description='Get contact by id',
    tags=['contact'],
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer    
    }

)
@api_view(['GET'])
@csrf_exempt
def get_contact_by_id(request, id):
    contact = None

    try:
        contact = Contact.objects.get(id=id)
    except Contact.DoesNotExist:

        logger.info(f'Contact not found id ({id})')

        return Response({
            'message': 'contact not found',
            'data': None,
            'errors': None
        }, status=status.HTTP_404_NOT_FOUND)
    
    contact_serializer = ContactSerializer(contact)
    
    return Response({
        'message':'success',
        'data': contact_serializer.data,
        'errors': None
    }, status=status.HTTP_200_OK)

@extend_schema(
    description='Create contact',
    tags=['contact'],
    request=ContactRequestSerializer,
    responses={
        201: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['POST'])
@csrf_exempt
def add_contact(request):
    contact_serializer = ContactRequestSerializer(data=request.data)

    if contact_serializer.is_valid():
        contact_serializer.save()
        return Response({
            'message': 'create contact success',
            'data': {
                'id': contact_serializer.data['id'],
            },
            'errors': None
        }, status=status.HTTP_201_CREATED)

    return Response({
        'errors': contact_serializer.errors,
        'message': 'create contact failed!',
        'data': None
    }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    description='Update contact',
    tags=['contact'],
    request=ContactRequestSerializer,
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['PUT'])
@csrf_exempt
def update_contact(request):
    id = request.data['id']
    contact = Contact.objects.get(id=id)
    if not contact:
        return Response({
            'message': 'contact not found',
            'data': None,
            'errors': None
        }, status=status.HTTP_404_NOT_FOUND)

    contact_serializer = ContactRequestSerializer(contact, data=request.data)
    if contact_serializer.is_valid():
        contact_serializer.save()
        return Response({
            'message': 'update contact success',
            'data': {
                'id': contact_serializer.data['id']
            },
            'errors': None
        }, status=status.HTTP_200_OK)

    return Response({
        'message': 'update contact failed',
        'data': None,
        'errors': contact_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    description='Delete contact',
    tags=['contact'],
    responses={
        200: ResponseAPISerializer,
        400: ResponseAPISerializer
    }
)
@api_view(['DELETE'])
@csrf_exempt
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    if not contact:
        return Response({
            'message': 'contact not found',
            'data': None,
            'errors': None
        }, status=status.HTTP_404_NOT_FOUND)
    
    contact.delete()
    response_api = ResponseAPISerializer({'message': 'delete contact success'})

    return Response(response_api.data, status=status.HTTP_200_OK)