from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate


class CheckAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        clear_token = False
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            if (token := request.COOKIES.get('token')) and (user := authenticate(request=request, token=token, not_api=True)):
                setattr(request, 'user', user)
            elif token:
                clear_token = True

        response = self.get_response(request)
        response.delete_cookie('token') if clear_token else None

        return response


class OAuth2TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            if not hasattr(request, 'user') or request.user.is_anonymous:
                if user := authenticate(request=request):
                    setattr(request, 'user', user)

    def process_response(self, request, response):
        patch_vary_headers(response, ('Authorization',))
        return response


def show_toolbar(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return True

    return False
