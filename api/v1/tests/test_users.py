from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import RequestsClient

from .test_items_base import TestItemsBase
from users.api import *

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