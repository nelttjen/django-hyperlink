from rest_framework import serializers
from django_hyperlink.serializers.default import DefaultSerializer

from users.serializers.profile import CurrentUserProfileSerializer


class LoginPostSerializer(DefaultSerializer):
    class LoginPostContentSerializer(serializers.Serializer):
        token = serializers.CharField(required=False)
        user = CurrentUserProfileSerializer(required=False)

    content = LoginPostContentSerializer(required=False)