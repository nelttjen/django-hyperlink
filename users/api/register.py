from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions
from django.contrib.auth.models import User

from django_hyperlink.public_settings import DOMAIN
from users.serializers.register import RegisterSerializer
from django_hyperlink.serializers.default import DefaultSerializer

from .swagger import *


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(
        operation_id='post-register',
        operation_description='Регистраци пользователя',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password', 'password_again'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password_again': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: RegisterPostSerializer(), 400: DefaultSerializer()}
    )
    def post(self, request):

        serializer = RegisterSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            raise ParseError(DefaultSerializer.get_error_message(serializer))
        serializer.create(serializer.validated_data)
        return Response(DefaultSerializer({
            'msg': 'Регистрация успешна! На ваш Email была отправлена ссылка для активации аккаунта',
            'content': serializer.data,
            'extra': {'link': f'{DOMAIN}/users/activate/'}
        }).data)

