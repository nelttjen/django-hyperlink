from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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
            user_id=self.superuser.id,
            key=self.superuser.username,
        )

        self.staff_user_token = Token.objects.create(
            user_id=self.staff_user.id,
            key=self.staff_user.username,
        )

        self.common_user_token = Token.objects.create(
            user_id=self.common_user.id,
            key=self.common_user.username,
        )