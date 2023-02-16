from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.serializers.default import DefaultSerializer
from django_hyperlink.modules.storage import MEDIA_STORAGE
from django_hyperlink.modules.uncashed_user import refresh_cache_user
from users.serializers.profile import UserProfileSerializer

from .swagger import *


class TestView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema()
    @refresh_cache_user
    def get(self, request):

        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': UserProfileSerializer(request.user.profile).data
        }).data)
