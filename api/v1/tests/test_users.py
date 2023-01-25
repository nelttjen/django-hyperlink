import copy

from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from rest_framework.test import RequestsClient

from django_hyperlink.public_settings import DOMAIN
from .test_items_base import TestItemsBase
from users.api import *
from users.models import User as CustomUser

client = RequestsClient()


class TestUsersCorrectView(TestCase):
    def test_users_activate_correct_view(self):
        url = reverse('api-users-activate')
        self.assertEqual(resolve(url).func.view_class, ActivateView)
        self.assertEqual(resolve(url).func.view_class.serializer_class, ActivateSerializer)

    def test_users_login_correct_view(self):
        url = reverse('api-users-login')
        self.assertEqual(resolve(url).func.view_class, LoginView)
        self.assertEqual(resolve(url).func.view_class.serializer_class, LoginSerializer)

    def test_users_recovery_correct_view(self):
        url = reverse('api-users-recovery')
        self.assertEqual(resolve(url).func.view_class, RecoveryView)
        self.assertEqual(resolve(url).func.view_class.serializer_class, RecoverySerializer)

    def test_users_register_correct_view(self):
        url = reverse('api-users-register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)
        self.assertEqual(resolve(url).func.view_class.serializer_class, RegisterSerializer)


class TestUsersCorrectUrl(TestCase):

    def _test_url(self, path):
        url = reverse(f'api-users-{path}')
        manual_url = f'/api/v1/users/{path}/'
        self.assertEqual(url, manual_url, msg=f'Пути {path} в текущем эндпоинте не совпадают')

    def test_users_activate_correct_url(self):
        self._test_url('activate')

    def test_users_login_correct_url(self):
        self._test_url('login')

    def test_users_recovery_correct_url(self):
        self._test_url('recovery')

    def test_users_register_correct_url(self):
        self._test_url('register')


class TestUsersResponding(TestCase, TestItemsBase):

    def setUp(self) -> None:
        self.create_users()

    def test_users_activate_responding(self):
        url = DOMAIN + reverse('api-users-activate')

        response = client.post(url)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def test_users_login_responding(self):
        url = DOMAIN + reverse('api-users-login')

        response = client.post(url)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def test_users_recovery_responding(self):
        url = DOMAIN + reverse('api-users-recovery')

        response = client.post(url)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

        response = client.put(url)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)

    def test_users_register_responding(self):
        url = DOMAIN + reverse('api-users-register')

        response = client.post(url)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 500)


class TestUsersCorrectWork(TestCase, TestItemsBase):

    def setUp(self) -> None:
        self.create_users()

        self.register_url = DOMAIN + reverse('api-users-register')

    def test_users_register_user_created(self):
        username = 'test'
        email = 'test@mail.ru'
        password = 'test_pass123'

        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_again': password
        }
        url = self.register_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        new_user = User.objects.filter(username=username).first()
        self.assertTrue(new_user)
        self.assertEqual(new_user.email, email)
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)

        new_custom = CustomUser.objects.filter(user_id=new_user.id).first()
        self.assertTrue(new_custom)

    def test_users_register_user_double_created(self):
        username = 'test'
        email = 'test@mail.ru'
        password = 'test_pass123'

        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_again': password
        }
        url = self.register_url

        self.assertEqual(User.objects.filter(username=username).count(), 0)

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        new_user = User.objects.filter(username=username).first()
        self.assertTrue(new_user)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

        response = client.post(url, data=data)

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

    def test_user_register_user_double_username(self):
        username = 'test'
        email1 = 'test1@mail.ru'
        email2 = 'test2@mail.ru'
        password = 'test_pass123'

        data1 = {
            'username': username,
            'email': email1,
            'password': password,
            'password_again': password
        }
        data2 = copy.copy(data1)
        data2['email'] = email2

        url = self.register_url

        self.assertEqual(User.objects.filter(username=username).count(), 0)

        response1 = client.post(url, data=data1)

        self.assertEqual(response1.status_code, 200)

        new_user = User.objects.filter(username=username).first()
        self.assertTrue(new_user)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

        response2 = client.post(url, data=data2)

        self.assertNotEqual(response2.status_code, 200)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

    def test_user_register_user_double_email(self):
        username1 = 'test1'
        username2 = 'test2'
        email = 'test@mail.ru'
        password = 'test_pass123'

        data1 = {
            'username': username1,
            'email': email,
            'password': password,
            'password_again': password
        }
        data2 = copy.copy(data1)
        data2['username'] = username2

        url = self.register_url

        self.assertEqual(User.objects.filter(email=email).count(), 0)

        response1 = client.post(url, data=data1)

        self.assertEqual(response1.status_code, 200)

        new_user = User.objects.filter(username=username1).first()
        self.assertTrue(new_user)
        self.assertEqual(User.objects.filter(email=email).count(), 1)

        response2 = client.post(url, data=data2)

        self.assertNotEqual(response2.status_code, 200)
        self.assertEqual(User.objects.filter(email=email).count(), 1)


