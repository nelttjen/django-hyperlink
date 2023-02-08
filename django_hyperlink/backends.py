from oauth2_provider.oauth2_backends import get_oauthlib_core
from rest_framework.authentication import BaseAuthentication
from oauth2_provider.models import AccessToken
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class APIAuth(BaseAuthentication):

    def authenticate(self, request, token=None, not_api=False):
        token = token or request.COOKIES.get('token')
        access_token = AccessToken.objects.filter(token=token).order_by('-id')

        if not access_token.exists():
            return None

        access_token = access_token.first()

        if access_token.is_expired():
            return None

        try:
            user = User.objects.get(pk=access_token.user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Пользователь не найден'))

        if not_api:
            return user

        return user, access_token.token


class OAuth2Authentication(BaseAuthentication):
    """
    OAuth 2 authentication backend using `django-oauth-toolkit`
    """

    www_authenticate_realm = 'api'

    @staticmethod
    def _dict_to_string(my_dict):
        return ','.join([f'{k}="{v}"' for k, v in my_dict.items()])

    def authenticate(self, request, **kwargs):
        """
        Returns two-tuple of (user, token) if authentication succeeds,
        or None otherwise.
        """
        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])

        if valid:
            return r.user, r.access_token

        request.oauth2_error = getattr(r, 'oauth2_error', {})

        return None

    def authenticate_header(self, request):
        """
        Bearer is the only finalized type currently
        """
        www_authenticate_attributes = {
            'realm': self.www_authenticate_realm
        }

        www_authenticate_attributes.update(
            getattr(request, 'oauth2_error', {})
        )

        return f'Bearer {self._dict_to_string(www_authenticate_attributes)}'
