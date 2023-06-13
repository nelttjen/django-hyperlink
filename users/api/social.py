import hashlib
import hmac

from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.public_settings import DOMAIN
from django_hyperlink.serializers.default import DefaultSerializer
from django_hyperlink.settings import TG_TOKEN
from users.serializers.profile import CurrentUserProfileSerializer
from users.modules import SocialAuth as AuthProvider, Auth, get_ip
from users.models import SocialStateCodes, Profile


def create_state(request):
    state = request.data.get('state')
    ip = get_ip(request)

    if state:
        state = SocialStateCodes(
            state=state,
            ip=ip
        )
        if request.user.is_authenticated:
            state.owner = request.user
        state.set_expire()
        state.save()


def confirm_state(request):
    state = request.data.get('state')
    ip = get_ip(request)
    
    print(ip)
    state = SocialStateCodes.objects.filter(state=state, ip=ip).first()
    
    if not state or state.is_expired():
        state.delete() if state else None
        raise ParseError(_('Сессия истекла, войдите заного'))
    state.delete()


class SocialAuthView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        if (provider := request.data.get('provider')) != 'tg':
            confirm_state(request)
        
        print(request.data)
        
        result = AuthProvider(request).authenticate()
        if isinstance(result, str):
            raise ParseError(_(result))

        user, data = result

        errors = {
            'vk': 'Вконтакте к профилю на сайте',
            'tg': 'Телеграм к профилю на сайте'
        }
        
        if not user:
            raise ParseError(_(f'Пользователь с такой привязкой не найден. '
                               f'Привяжите {errors[provider]} и повторите авторизацию'))

        token = Auth(user, request).authenticate()

        return Response(DefaultSerializer(
            {'content': {'token': token, 'profile': CurrentUserProfileSerializer(user.profile).data}}
        ).data)

    def put(self, request):
        create_state(request)
        return Response(DefaultSerializer({'msg': 'ok'}).data)


class SocialUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        if request.data.get('provider') != 'tg':
            confirm_state(request)

        result = AuthProvider(request).authenticate()
        if isinstance(result, str):
            raise ParseError(_(result))

        user, data = result

        if user:
            raise ParseError(_('Эта социальная сеть уже привязана к другому профилю'))

        provider = request.data.get('provider')

        update = {AuthProvider.PROVIDERS[provider]: data[AuthProvider.PROVIDERS[provider]]}
        
        Profile.objects.filter(user_id=request.user.id).update(**update)
        
        return Response(DefaultSerializer({'content': update}).data)

    def put(self, request):
        create_state(request)
        return Response(DefaultSerializer({'msg': 'ok'}).data)

    def delete(self, request):
        provider = request.data.get('provider')
        if provider not in AuthProvider.PROVIDERS:
            raise ParseError(_('Такого провайдера нет'))

        Profile.objects.filter(user_id=request.user.id).update(
            **{AuthProvider.PROVIDERS[provider]: None}
        )
        return Response(DefaultSerializer({'msg': 'ok'}).data)
    