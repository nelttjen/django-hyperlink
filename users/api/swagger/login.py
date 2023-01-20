from rest_framework import serializers
from django_hyperlink.serializers.default import DefaultSerializer


class LoginPostSerializer(DefaultSerializer):
    class LoginPostContentSerializer(serializers.Serializer):
        token = serializers.CharField(required=False)
        username = serializers.CharField(required=False)

    content = LoginPostContentSerializer(required=False)