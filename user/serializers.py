from rest_framework import serializers
from django.contrib.auth.models import User
from contact.serializers import ContactSerializer

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        write_only_fields = ['password']

class UserSerializer(serializers.ModelSerializer):
    user_contact = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_contact']
        write_only_fields = ['password']