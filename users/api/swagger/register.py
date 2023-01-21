from rest_framework import serializers

from django_hyperlink.serializers.default import DefaultSerializer
from users.serializers.register import RegisterSerializer


class RegisterPostSerializer(DefaultSerializer):
    class RegisterPostExtraSerializer(serializers.Serializer):
        link = serializers.CharField(required=False)

    content = RegisterSerializer(required=False)
    extra = RegisterPostExtraSerializer(required=False)
