from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from users.serializers.login import LoginSerializer
from django_hyperlink.serializers.default import DefaultSerializer

from .swagger import *


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id='post-login',
        operation_description='Получение токена пользователя для последующей авторизации в другие эндпоинты',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: LoginPostSerializer(), 400: DefaultSerializer()}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, request=request)
        if not serializer.is_valid():
            raise ParseError(DefaultSerializer.get_error_message(serializer))
        result = serializer.login()
        return Response(DefaultSerializer({
            'msg': "ok",
            'content': result
        }).data)