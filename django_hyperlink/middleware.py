from django_hyperlink.settings import DEBUG

from rest_framework.authtoken.models import Token


def show_toolbar(request):
    if 'Token' in request.COOKIES.keys():
        token = request.COOKIES['Token']
        token = Token.objects.filter(key=token).first()
        if token:
            setattr(request, 'user', token.user)

    if request.user.is_authenticated and request.user.is_superuser:
        return True

    return False
