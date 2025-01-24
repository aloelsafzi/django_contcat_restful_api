from rest_framework import serializers
from contact.models import Contact

class ContactRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'phone', 'first_address', 'seconds_address', 'user']

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'phone', 'first_address', 'seconds_address']