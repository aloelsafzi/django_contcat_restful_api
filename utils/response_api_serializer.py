from rest_framework import serializers

class ResponseAPISerializer(serializers.Serializer):
    message = serializers.CharField(default='')
    data = serializers.DictField(default={})
    errors = serializers.ListField(default=[])