import datetime

from django.contrib.auth.models import User
from django.utils import timezone
# from rest_framework.authtoken.models import Token
from oauth2_provider.models import AccessToken as Token

class TestItemsBase:
    def create_users(self):
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@testmail.com',
            password='superuser'
        )

        self.staff_user = User.objects.create_user(
            username='staff_user',
            email='staff_user@testmail.com',
            password='staff_user',
            is_staff=True
        )

        self.common_user = User.objects.create_user(
            username='common_user',
            email='common_user@testmail.com',
            password='common_user',
        )

        self.superuser_token = Token.objects.create(
            user=self.superuser,
            token=self.superuser.username,
            expires=timezone.now() + datetime.timedelta(days=365),
            scope='all',
        )

        self.staff_user_token = Token.objects.create(
            user=self.staff_user,
            token=self.staff_user.username,
            expires=timezone.now() + datetime.timedelta(days=365),
            scope='all',
        )

        self.common_user_token = Token.objects.create(
            user=self.common_user,
            token=self.common_user.username,
            expires=timezone.now() + datetime.timedelta(days=365),
            scope='all',
        )