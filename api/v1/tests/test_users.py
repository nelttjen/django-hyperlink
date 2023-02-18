import copy
import datetime
import logging
import time

from unittest.mock import patch
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from django.utils import timezone
from oauth2_provider.models import AccessToken
from rest_framework.test import RequestsClient

from django_hyperlink.settings import DOMAIN, DATABASES
from users.api import *
from users.tasks import *
from users.models import Profile as CustomUser, ActivateCode
from users.modules import PasswordValidator
from .test_items_base import TestItemsBase

client = RequestsClient()
logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)
logging.disable(logging.WARNING)
logging.disable(logging.WARN)
logging.disable(logging.ERROR)


print(f'Stating user tests using db backend: {DATABASES["default"]["ENGINE"]}')


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
        self.activate_url = DOMAIN + reverse('api-users-activate')
        self.login_url = DOMAIN + reverse('api-users-login')
        self.recovery_url = DOMAIN + reverse('api-users-recovery')

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

        code = ActivateCode.objects.filter(user_id=new_user.id, is_used=False, type=1).first()
        self.assertTrue(code)
        self.assertGreater(code.expired_date, timezone.now())

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

    def test_user_register_username_error(self):
        data = {
            'username': 'us',
            'email': 'mail@mail.mail',
            'password': 'pass123123',
            'password_again': 'pass123123'
        }

        url = self.register_url

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='us').first())

    def test_user_register_username_regex_error(self):
        username = '@#$@$%#$^$%$%#$^#$'
        data = {
            'username': username,
            'email': 'mail@mail.mail',
            'password': 'pass123123',
            'password_again': 'pass123123'
        }

        url = self.register_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username=username).first())

    def test_user_register_password_error(self):
        data = {
            'username': 'username123',
            'email': 'mail@mail.mail',
            'password': '1',
            'password_again': '1'
        }

        url = self.register_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='us').first())
        self.assertIsInstance(PasswordValidator('1', '1').validate(), str)

    def test_user_register_password_noteq(self):
        data = {
            'username': 'username123',
            'email': 'mail@mail.mail',
            'password': 'Password_123',
            'password_again': 'Password_1234'
        }

        url = self.register_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='us').first())

    def test_user_activate(self):
        user = User.objects.create_user(
            username='test',
            email='test@test.test',
            password='test',
            is_active=False,
        )

        code = ActivateCode.objects.create(
            type=1,
            user=user,
        )

        data = {'code': code.code}

        url = self.activate_url

        response = client.post(url, data=data)
        # celery task using test db
        activate_user(code.code)

        self.assertEqual(response.status_code, 200)

        new_user = User.objects.get(pk=user.pk)
        new_code = ActivateCode.objects.get(pk=code.pk)

        self.assertTrue(new_user.is_active)
        self.assertTrue(new_code.is_used)
        self.assertIsNotNone(new_code.activated_date)
        self.assertEqual(new_code.type, 1)

    def test_user_activate_expired(self):
        user = User.objects.create_user(
            username='test',
            email='test@test.test',
            password='test',
            is_active=False,
        )

        code = ActivateCode.objects.create(
            type=1,
            user=user,
        )
        ActivateCode.objects.filter(id=code.id).update(
            expired_date=timezone.now() - datetime.timedelta(days=9999)
        )

        data = {'code': code.code}

        url = self.activate_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        new_user = User.objects.get(pk=user.id)

        self.assertFalse(new_user.is_active)
        self.assertFalse(ActivateCode.objects.filter(id=code.id).exists())

    def test_user_activate_invalid_code(self):
        user = User.objects.create_user(
            username='test',
            email='test@test.test',
            password='test',
            is_active=False,
        )

        data = {'code': 'fsdfsdfsaSFS'}
        url = self.activate_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        new_user = User.objects.get(pk=user.pk)

        self.assertFalse(new_user.is_active)

    def test_user_activate_use_other_code_type(self):
        user = User.objects.create_user(
            username='test',
            email='test@test.test',
            password='test',
            is_active=False,
        )

        code = ActivateCode.objects.create(
            type=2,
            user_id=user.id,
        )

        data = {'code': code.code}

        url = self.activate_url

        response = client.post(url, data=data)

        new_user = User.objects.get(pk=user.pk)
        new_code = ActivateCode.objects.get(pk=code.pk)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_code.is_used)
        self.assertEqual(new_code.type, 2)
        self.assertGreater(new_code.expired_date, timezone.now())

    def test_user_login(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True
        )

        data = {
            'username': usr, 'password': pwd
        }
        url = self.login_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        token = AccessToken.objects.filter(user_id=user.id).first()

        self.assertEqual(response.json()['content']['token'], token.token)
        self.assertEqual(response.json()['content']['user']['username'], user.username)

    def test_user_login_by_email(self):
        mail = 'login@test.com'
        pwd = 'login_password'
        user = User.objects.create_user(
            username='login',
            email=mail,
            password=pwd,
            is_active=True
        )

        data = {
            'username': mail, 'password': pwd
        }
        url = self.login_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        token = AccessToken.objects.filter(user_id=user.id).first()

        self.assertEqual(response.json()['content']['token'], token.token)
        self.assertEqual(response.json()['content']['user']['username'], user.username)

    def test_user_login_banned(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True,
        )
        custom_user = CustomUser.objects.get(user_id=user.id)
        custom_user.ban = {'is_banned': True, 'ban_until': None, 'ban_message': None}
        custom_user.save()

        url = self.login_url
        data = {'username': usr, 'password': pwd}

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('заблокирован', response.json()['errors']['msg'].lower())
        self.assertIn('навсегда', response.json()['errors']['msg'].lower())

        custom_user.ban = {'is_banned': True,
                           'ban_until': datetime.datetime(day=20, month=2, year=2028).timestamp(),
                           'ban_message': None}
        custom_user.save()

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('заблокирован', response.json()['errors']['msg'].lower())
        self.assertIn('20.02.2028', response.json()['errors']['msg'].lower())

        custom_user.ban = custom_user.ban_json
        custom_user.save()

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['content']['token'])
        self.assertEqual(response.json()['content']['user']['username'], user.username)

    def test_users_login_ban_expired(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True,
        )
        custom_user = CustomUser.objects.get(user_id=user.id)
        custom_user.ban = {'is_banned': True,
                           'ban_until': datetime.datetime(day=1, month=1, year=1999).timestamp(),
                           'ban_message': None}
        custom_user.save()

        url = self.login_url
        data = {'username': usr, 'password': pwd}

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['content']['token'])
        self.assertEqual(response.json()['content']['user']['username'], user.username)

        updated = CustomUser.objects.get(pk=custom_user.id)
        self.assertFalse(updated.ban['is_banned'])
        self.assertIsNone(updated.ban['ban_until'])
        self.assertIsNone(updated.ban['ban_message'])

    def test_login_no_such_user(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True,
        )

        url = self.login_url
        data = {'username': usr + "sfsf", 'password': pwd}

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_user_login_invalid_username(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True,
        )

        url = self.login_url
        data = {'username': usr + "sfsf", 'password': pwd}

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_user_login_invalid_password(self):
        usr = 'login'
        pwd = 'login_password'
        user = User.objects.create_user(
            username=usr,
            email='login@test.com',
            password=pwd,
            is_active=True,
        )

        url = self.login_url
        data = {'username': usr, 'password': pwd + "sfsf"}

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_users_recovery_post(self):
        user = self.common_user

        data = {'username': user.username}
        url = self.recovery_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(ActivateCode.objects.filter(
            user_id=user.id, type=2, is_used=False, expired_date__gt=timezone.now()
        ).exists())

    def test_users_recovery_post_fake_username(self):
        user = self.common_user

        data = {'username': user.username + '123'}
        url = self.recovery_url

        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        self.assertFalse(ActivateCode.objects.filter(
            user__username=user.username, type=2, is_used=False, expired_date__gt=timezone.now()
        ).select_related('user').exists())

    def test_users_recovery_put(self):
        user = self.common_user

        data = {'username': user.username}
        url = self.recovery_url

        response_post = client.post(url, data=data)

        self.assertEqual(response_post.status_code, 200)

        code = ActivateCode.objects.filter(
            user_id=user.id, type=2, is_used=False, expired_date__gt=timezone.now()
        ).first()
        self.assertTrue(code)

        new_pass = 'TestNewPass_123'
        data_put = {'code': code.code, 'password': new_pass, 'password_again': new_pass}

        self.assertTrue(user.check_password('common_user'))

        response_put = client.put(url, data=data_put)

        # celery task using correct db
        recovery_user(code_id=code.id, user_id=code.user.id, password=new_pass)

        self.assertEqual(response_put.status_code, 200)
        self.assertTrue(ActivateCode.objects.get(pk=code.id).is_used)

        changed_user = User.objects.get(pk=user.id)

        self.assertNotEqual(user.password, changed_user.password)

        data_login = {'username': changed_user.username, 'password': new_pass}
        url_login = self.login_url

        response_login = client.post(url_login, data=data_login)

        self.assertEqual(response_login.status_code, 200)
        self.assertTrue(changed_user.check_password(new_pass))
        self.assertFalse(changed_user.check_password('common_user'))
        self.assertEqual(response_login.json()['content']['user']['username'], user.username)

    def test_users_recovery_put_code_used(self):
        user = self.common_user

        code = ActivateCode.objects.create(
            user_id=user.id, type=2
        )
        ActivateCode.objects.filter(id=code.id).update(is_used=True)

        url = self.recovery_url
        new_pass = 'TestPass123'

        self.assertTrue(user.check_password('common_user'))

        response = client.put(url, data={'code': code.code, 'password': new_pass, 'password_again': new_pass})

        self.assertEqual(response.status_code, 400)

        updated_user = User.objects.get(pk=user.id)
        self.assertTrue(updated_user.check_password('common_user'))
        self.assertFalse(updated_user.check_password(new_pass))

    def test_users_recovery_put_code_expired(self):
        user = self.common_user

        code = ActivateCode.objects.create(
            user_id=user.id, type=2
        )
        ActivateCode.objects.filter(id=code.id).update(expired_date=timezone.now() - datetime.timedelta(days=365))

        url = self.recovery_url
        new_pass = 'TestPass123'

        self.assertTrue(user.check_password('common_user'))

        response = client.put(url, data={'code': code.code, 'password': new_pass, 'password_again': new_pass})

        self.assertEqual(response.status_code, 400)

        updated_user = User.objects.get(pk=user.id)
        self.assertTrue(updated_user.check_password('common_user'))
        self.assertFalse(updated_user.check_password(new_pass))
        self.assertFalse(ActivateCode.objects.filter(id=code.id).exists())

    def test_users_recovery_put_password_xyuni(self):
        user = self.common_user

        code = ActivateCode.objects.create(
            user_id=user.id, type=2
        )

        url = self.recovery_url
        new_pass = '1'

        self.assertTrue(user.check_password('common_user'))

        response = client.put(url, data={'code': code.code, 'password': new_pass, 'password_again': new_pass})

        self.assertEqual(response.status_code, 400)

        updated_user = User.objects.get(pk=user.id)
        self.assertIsInstance(PasswordValidator(new_pass, new_pass).validate(), str)
        self.assertTrue(updated_user.check_password('common_user'))
        self.assertFalse(updated_user.check_password(new_pass))


class TestCeleryTasks(TestCase, TestItemsBase):

    def setUp(self) -> None:
        self.create_users()

    def test_celery_send_email_prime(self):
        result = send_activation_code(
            email='test@mail.ru',
            subject='test',
            message='test',
            fail_silently=False
        )

        self.assertTrue(result)

    @patch('users.tasks.user_code.send_mail')
    def test_celery_mock_send_email_true(self, mock_send):
        mock_send.return_value = 1

        result = send_activation_code(
            email='test@mail.ru',
            subject='test',
            message='test',
            fail_silently=False
        )

        self.assertTrue(result)

    @patch('users.tasks.user_code.send_mail')
    def test_celery_mock_send_email_false(self, mock_send):
        mock_send.return_value = 0

        result = send_activation_code(
            email='test@mail.ru',
            subject='test',
            message='test',
            fail_silently=False
        )

        self.assertFalse(result)

    def test_celery_activate_prime(self):
        user = self.common_user
        user.is_active = False
        user.save()

        code = ActivateCode.objects.create(
            type=1, user_id=user.id
        )

        result = activate_user(code=code.code)

        updated_user = User.objects.get(pk=user.id)
        updated_code = ActivateCode.objects.get(pk=code.id)

        self.assertTrue(result)
        self.assertTrue(updated_user.is_active)
        self.assertTrue(updated_code.is_used)
        self.assertIsNotNone(updated_code.activated_date)

    def test_celery_activate_user(self):
        user = self.common_user

        code = ActivateCode.objects.create(
            type=2, user_id=user.id
        )
        new_password = 'TestSuperPass123'

        self.assertTrue(user.check_password('common_user'))

        result = recovery_user(code_id=code.id, user_id=user.id, password=new_password)

        updated_user = User.objects.get(pk=user.id)
        updated_code = ActivateCode.objects.get(pk=code.id)

        self.assertTrue(result)
        self.assertNotEqual(updated_user.password, user.password)
        self.assertTrue(updated_code.is_used)
        self.assertIsNotNone(updated_code.activated_date)
        self.assertTrue(updated_user.check_password(new_password))
        self.assertFalse(updated_user.check_password('common_user'))