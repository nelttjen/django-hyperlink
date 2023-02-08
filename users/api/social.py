from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.serializers.default import DefaultSerializer
from users.modules import SocialAuth as AuthProvider, Auth
from users.models import SocialStateCodes


class SocialAuthView(APIView):
    permission_classes = (permissions.AllowAny, )

    def _get_request_source(self, request):
        return request.META.get('HTTP_CF_CONNECTING_IP') or \
               request.META.get('REMOTE_HOST') or \
               request.META.get('REMOTE_ADDR')

    def post(self, request):
        state = request.data.get('state')
        ip = self._get_request_source(request)

        state = SocialStateCodes.objects.filter(state=state, ip=ip).first()
        if not state or state.is_expired():
            state.delete() if state else None
            raise ParseError(_('Сессия истекла, войдите заного'))
        state.delete()

        result = AuthProvider(request).authenticate()
        if isinstance(result, str):
            raise ParseError(_(result))

        user, data = result

        errors = {
            'vk': 'Вконтакте к профилю на сайте'
        }

        if not user:
            raise ParseError(_(f'Пользователь с такой привязкой не найден. '
                               f'Привяжите {errors[request.data.get("provider")]} и повторите авторизацию'))

        token = Auth(user, request).authenticate()

        return Response(DefaultSerializer({'content': {'token': token, 'username': user.username}}).data)

    def put(self, request):
        state = request.data.get('state')
        ip = self._get_request_source(request)

        if state:
            state = SocialStateCodes(
                state=state,
                ip=ip
            )
            state.set_expire()
            state.save()

        return Response(DefaultSerializer({'msg': 'ok'}).data)