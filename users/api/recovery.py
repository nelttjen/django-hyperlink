from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.public_settings import DOMAIN
from users.serializers.recovery import RecoverySerializer
from django_hyperlink.serializers.default import DefaultSerializer

from .swagger import *


class RecoveryView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = RecoverySerializer

    @swagger_auto_schema(
        operation_id='post-recovery',
        operation_description='Генерация кода для восстановления пароля пользователя (по почте или никнейму)',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: RecoveryPostSerializer(), 400: DefaultSerializer()}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, method='post')
        if not serializer.is_valid():
            raise ParseError(DefaultSerializer.get_error_message(serializer))
        serializer.send_mail()
        return Response(DefaultSerializer({
            'msg': 'На ваш email, указанный при регистрации был отправлен код подтверждения'
        }).data)

    @swagger_auto_schema(
        operation_id='put-recovery',
        operation_description='Восстановление пароля по коду',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['code', 'password', 'password_again'],
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password_again': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: RecoveryPutSerializer(), 400: DefaultSerializer()}
    )
    def put(self, request):
        serializer = self.serializer_class(data=request.data, method='put')
        if not serializer.is_valid():
            raise ParseError(DefaultSerializer.get_error_message(serializer))
        serializer.recovery_user()
        return Response(DefaultSerializer({
            'msg': 'Пароль изменен. Теперь вы можете войти, используя новый пароль',
            'content': {
                "link": f"{DOMAIN}/users/login/"
            }
        }).data)