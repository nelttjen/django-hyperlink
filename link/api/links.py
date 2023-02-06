from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from link.serializers.links import ShareLinkSerializer
from django_hyperlink.serializers.default import DefaultSerializer


class LinkView(APIView):
    permission_classes = (permissions.AllowAny, )

    serializer_class = ShareLinkSerializer

    def get(self, request, code):
        link = self.serializer_class.get_link(request, code)

        if not link:
            raise ParseError(_('Ссылка не найдена, истекла или достигла лимита перенаправлений.'))

        is_owner = request.user.is_authenticated and request.user.id == link.owner_id

        return Response(DefaultSerializer({
            'content': self.serializer_class(link, is_owner=is_owner).data
        }).data)

    def post(self, request, code):

        self.serializer_class.redirect(request, code)

        return Response(DefaultSerializer({
            'msg': 'ok'
        }).data)