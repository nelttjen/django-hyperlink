from rest_framework import serializers
from django_hyperlink.serializers.default import DefaultSerializer


class RecoveryPostSerializer(DefaultSerializer):
    pass


class RecoveryPutSerializer(DefaultSerializer):
    class RecoveryPutContentSerializer(serializers.Serializer):
        link = serializers.CharField(required=False)

    content = RecoveryPutContentSerializer(required=False)