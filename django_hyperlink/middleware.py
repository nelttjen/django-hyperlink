from django_hyperlink.settings import DEBUG


def show_toolbar(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return True
    return False
