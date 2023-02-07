import datetime
import random
import string

from django.http import QueryDict
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_hyperlink.serializers.default import DefaultSerializer
from link.serializers.links import ShareLinkSerializer, ShareLinkCreateSerializer


class LinkView(APIView):
    permission_classes = (permissions.AllowAny, )

    serializer_class = ShareLinkSerializer

    def get(self, request, code):
        link = self.serializer_class.get_link(request, code)

        if not link:
            from django.utils.translation import gettext_lazy as _
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


class LinkCreateView(CreateAPIView, UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ShareLinkCreateSerializer

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True

        data = request.data.copy()

        exclude = ['redirects', 'date_created', 'share_code', ]
        if request.user.is_authenticated:
            request.data['owner'] = request.user.id
        else:
            exclude += ['redirect_timer', 'valid_until', 'allowed_redirects', 'owner',
                        'only_unique_redirects', 'is_active']

        for key in data.keys():
            if key in exclude:
                request.data.pop(key)

        request.data['share_code'] = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])

        def none_int(x): return int(x) if x is not None else None

        if (valid := none_int(request.data.get('valid_until', 7))) not in (1, 7, 30, None):
            from django.utils.translation import gettext_lazy as _
            raise ParseError(_('Ссылка должна быть действительна в течении  1, 7 или 30 дней или быть бессрочной'))

        request.data['valid_until'] = timezone.now() + datetime.timedelta(days=valid) if valid else None

        if 'is_active' not in request.data:
            request.data['is_active'] = True

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.utils.translation import gettext_lazy as _
            return NotAuthenticated(_('Для редактирования нужно авторизоваться'))

        return self.update(request, *args, **kwargs)