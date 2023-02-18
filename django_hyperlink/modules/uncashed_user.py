import functools

from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache
from oauth2_provider.models import AccessToken


def refresh_cache_user(func):
    @functools.wraps(func)
    def inner_func(view, request, *args, **kwargs):
        if request.user.is_authenticated:
            # request.user = User.objects.select_related('profile').get(pk=request.user.pk)
            token = AccessToken.objects.filter(user_id=request.user.id).select_related('user', 'user__profile').first()
            if not token:
                request.user = AnonymousUser()
            else:
                request.user = token.user
                cache.set(f'token-{token.token}', token, 3600)
                cache.set(f'oauth2-token-{token.token}', token, 3600)

        return func(view, request, *args, **kwargs)

    return inner_func
