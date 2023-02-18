import datetime
import math
import random
import string

from django.db.models import F, IntegerField
from django.db.models.functions import Cast, Extract
from django.http import QueryDict
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.exceptions import ParseError, NotAuthenticated, ValidationError
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_hyperlink.serializers.default import DefaultSerializer
from link.models import ShareLink, LinkRedirect
from link.serializers.links import ShareLinkSerializer, ShareLinkUpdateSerializer


class MyLinkView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def _get_link(self, request, link_id):
        link = ShareLink.objects.filter(id=link_id).first()

        if not link or link.owner_id != request.user.id:
            raise ParseError(_('Ссылка не найдена'))
        return link

    def get(self, request, link_id):
        link = self._get_link(request, link_id)

        return Response(DefaultSerializer({'content': ShareLinkSerializer(link, is_owner=True).data}).data)

    def put(self, request, link_id):
        link = self._get_link(request, link_id)

        serializer = ShareLinkUpdateSerializer(data=request.data, instance=link)
        serializer.is_valid(raise_exception=True)
        link = serializer.save()

        return Response(DefaultSerializer({'content': ShareLinkSerializer(link, is_owner=True).data}).data)

    def delete(self, request, link_id):
        link = self._get_link(request, link_id)

        link.delete()

        return Response(DefaultSerializer({'msg': 'deleted'}).data)


class MyLinkListView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        data = request.GET
        filters = {
            'owner_id': request.user.id
        }

        ord_list = ('date_created', 'valid_until', 'allowed_redirects',
                     'redirects', 'only_unique_redirects', 'is_active')
        ords = []
        for item in ord_list:
            ords.extend([item, f'-{item}'])

        if (ordering := data.get('ordering')) not in ords:
            ordering = '-date_created'

        if (active := data.get('active')) is not None:
            filters['is_active'] = bool(int(active))

        if bool(int(data.get('not_expired', 0))):
            filters['valid_until__gt'] = timezone.now()

        try:
            count = max(min(int(data.get('count', 20)), 20), 1)
            page = int(data.get('page', 1))
        except:
            count = 20
            page = 1

        links = ShareLink.objects.filter(**filters).order_by(ordering).annotate(
            date_created_as_timestamp=Cast(Extract('date_created', 'epoch'), IntegerField()),
            valid_until_as_timestamp=Cast(Extract('valid_until', 'epoch'), IntegerField())
        )

        total = links.count()
        extra = {
            'total_count': total,
            'total_pages': math.ceil(total / count),
            'current_page': page
        }

        links = links[count*(page-1):count*page]

        return Response(DefaultSerializer({
            'content': ShareLinkSerializer(links, many=True, is_owner=True, add_timestamp=True).data,
            'extra': extra
        }).data)

