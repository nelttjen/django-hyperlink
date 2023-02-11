from django.utils import timezone
from oauth2_provider.oauth2_backends import get_oauthlib_core
from rest_framework.authentication import BaseAuthentication
from oauth2_provider.models import AccessToken
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from users.models import Profile


class APIAuth(BaseAuthentication):

    def authenticate(self, request, token=None, not_api=False):
        token = token or request.COOKIES.get('token')

        if not token:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')

        access_token = AccessToken.objects.filter(token=token).select_related('user', 'user__profile').order_by('-id').first()

        if not access_token:
            return None

        if access_token.is_expired():
            return None

        user = access_token.user
        update_last_seen(user)

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
            user = User.objects.filter(pk=r.user.pk).select_related('profile').first()
            update_last_seen(user)
            return user, r.access_token

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


def update_last_seen(user):
    try:
        profile_id = user.profile.id
    except:
        pass
    else:
        Profile.objects.filter(id=profile_id).select_for_update().update(
            last_seen=timezone.now()
        )