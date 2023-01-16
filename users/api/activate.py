from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from users.serializers.activate import ActivateSerializer
from django_hyperlink.serializers.default import DefaultSerializer
from django_hyperlink.settings import DOMAIN

from .swagger import *


class ActivateView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(
        operation_id='post-activate',
        operation_description='Активировать пользователя по коду',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['code'],
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: ActivatePostSerializer(), 400: DefaultSerializer()}
    )
    def post(self, request):

        serializer = ActivateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError(DefaultSerializer.get_error_message(serializer))
        serializer.activate()
        redirect_msg = 'Пользователь активирован. Теперь вы можете войти в систему'
        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': {'redirect': f'{DOMAIN}/users/login/', 'redirect_msg': redirect_msg},
        }).data)
