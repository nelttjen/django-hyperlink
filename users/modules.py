import re

from django.contrib.auth.models import User
from django.utils import timezone

from django_hyperlink.public_settings import DOMAIN
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
