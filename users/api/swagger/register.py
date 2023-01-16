from django_hyperlink.serializers.default import DefaultSerializer
from users.serializers.register import RegisterSerializer


class RegisterPostSerializer(DefaultSerializer):
    content = RegisterSerializer(required=False)
