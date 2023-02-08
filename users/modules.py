import datetime
import re

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from oauth2_provider.models import AccessToken, RefreshToken, Application

from django_hyperlink.settings import DOMAIN, DEBUG, OAUTH2_DEFAULT_APP, OAUTH2_PROVIDER
from users.models import ActivateCode
from users.tasks.user_code import send_activation_code


class Email:
	def __init__(self, user_id):
		self.user = User.objects.filter(id=user_id).first()

	def generate_code(self, code_type):
		if not (code := ActivateCode.objects.filter(user=self.user, is_used=False,
		                                            expired_date__gte=timezone.now(),
		                                            type=code_type).first()):
			code = ActivateCode(user=self.user, type=code_type).generate_code()
		return code

	def send_mail_base(self, subject, message):
		email = self.user.email
		send_activation_code.delay(email, subject, message)

	def send_activation_mail(self):
		if not self.user:
			return False

		code = self.generate_code(code_type=1)
		subject = 'Завершение регистрации'
		message = f'Здравствуйте! Ваша ссылка для регистрации аккаунта: {DOMAIN}/users/activate/?code={code.code}. ' \
		          f'Ссылка действительна в течении {code.expired_min} минут. Код для активации: {code.code}'
		self.send_mail_base(subject, message)
		return True

	def send_recovery_mail(self):
		if not self.user:
			return False

		code = self.generate_code(code_type=2)
		subject = 'Восстановление аккаунта'
		message = f'Здравствуйте! Ваша ссылка для восстановления аккаунта: {DOMAIN}/users/recovery/?code={code.code}. ' \
		          f'Ссылка действительна в течении {code.expired_min} минут. Код для восстановления: {code.code}'
		self.send_mail_base(subject, message)


class PasswordValidator:
	def __init__(self, pass1, pass2):
		self.pass1 = pass1
		self.pass2 = pass2

		self.validator = re.compile(r'^[A-Za-z0-9_#@$&*-]{3,50}$')

	def validate(self) -> str | bool:
		if not self.validator.fullmatch(self.pass1):
			return 'Пароль должен быть 3-50 символов и ' \
			       'содержать в себе только буквы латинского алфавита, а также символы _#@$&*-'
		if self.pass1 != self.pass2:
			return 'Пароли не совпадают'
		return True


class Auth:
	def __init__(self):
		self.user = None
		self.request = None

	def _create_token(self):

		try:
			app = Application.objects.get(pk=OAUTH2_DEFAULT_APP)
			new = AccessToken.objects.create(
				user_id=self.user.id,
				token=random_token_generator(self.request),
				application_id=app.id,
				expires=timezone.now() + datetime.timedelta(seconds=OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']),
				scope='all'
			)

			RefreshToken.objects.create(
				user_id=self.user.id,
				access_token_id=new.id,
				application_id=app.id,
				token=random_token_generator(self.request),
			)
		except Application.DoesNotExist:
			new = AccessToken.objects.create(
				user_id=self.user.id,
				token=random_token_generator(self.request),
				expires=timezone.now() + datetime.timedelta(days=1),
				scope='all'
			)

		return new

	def authenticate(self):
		if not self.user:
			raise Exception('Пользователь не был проверен перед авторизацией')
		if not self.request:
			raise Exception('Попытка авторизации без реквеста')

		token = AccessToken.objects.filter(user_id=self.user.id).order_by('-id').first()

		if not token:
			token = self._create_token()
		elif token.is_expired():
			token.delete()
			token = self._create_token()

		return token.token

	def authenticate_user(self, username, password):
		if not username or not password:
			return 'Не переданы данные для авторизации'
		user = User.objects.filter(Q(username=username) | Q(email=username)).first()
		if not user:
			return 'Неверный логин или пароль'
		if not user.check_password(password):
			return 'Неверный логин или пароль'
		if not user.is_active:
			return 'На вашу почту было выслано письмо с кодом подтверждения'
		ban, msg = user.user.check_ban()
		if ban:
			return msg
		self.user = user
