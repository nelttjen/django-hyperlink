from django.db.models import F
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate

from users.modules import get_ip
from users.models import UserHistory, DjangoUser


class CheckAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        clear_token = False
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            if (token := request.COOKIES.get('token')) and (user := authenticate(request=request, token=token, not_api=True)):
                setattr(request, 'user', user)
                check_user_history(request, user)
            elif token:
                clear_token = True

        response = self.get_response(request)
        response.delete_cookie('token') if clear_token else None

        return response


class OAuth2TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            if not hasattr(request, 'user') or request.user.is_anonymous:
                if user := authenticate(request=request, not_api=True):
                    user = DjangoUser.objects.filter(pk=user.id).select_related('profile').first()
                    setattr(request, 'user', user)
                    check_user_history(request, user)

    def process_response(self, request, response):
        patch_vary_headers(response, ('Authorization',))
        return response


def show_toolbar(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return True

    return False


def check_user_history(request, user):
    ip = get_ip(request)

    if user.profile.last_ip != ip:
        user.profile.last_ip = ip
        user.profile.save()

        profile_id = user.profile.id
        history_mark = UserHistory.objects.filter(
            profile_id=profile_id,
            ip=ip
        )

        if not history_mark.exists():
            UserHistory.objects.create(
                profile_id=profile_id,
                ip=ip,
                count=1
            )
        else:
            history_mark.update(
                count=F('count') + 1
            )