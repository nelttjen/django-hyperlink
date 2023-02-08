from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import ActivateCode
from users.tasks.user_code import recovery_user
from users.modules import Email, PasswordValidator


class RecoverySerializer(serializers.Serializer):

	def __init__(self, *args, **kwargs):
		self.method = kwargs.pop('method')
		super().__init__(*args, **kwargs)

	def validate(self, attrs):
		if self.method == 'post':
			username = self.initial_data.get('username', None)
			email = self.initial_data.get('email', None)
			if not any([username, email]):
				raise ValidationError('Данные не предоставлены')
			if not (user := User.objects.filter(Q(username=username) | Q(email=email)).first()):
				raise ValidationError('Пользователь не найден')
			self.user = user
		elif self.method == 'put':
			code = self.initial_data.get('code', None)
			pass1 = self.initial_data.get('password', '')
			pass2 = self.initial_data.get('password_again', '')
			if isinstance((validate := PasswordValidator(pass1, pass2).validate()), str):
				raise ValidationError(validate)
			if not (code := ActivateCode.objects.filter(code__iexact=code,
			                                            is_used=False, type=2).first()):
				raise ValidationError('Код не найден или был использован')
			if code.expired_date < timezone.now():
				Email(code.user.id).send_recovery_mail()
				code.delete()
				raise ValidationError('Код устарел. Новый код был отправлен на email, указаный при регистрации')
			self.code = code
		return self.initial_data

	def send_mail(self):
		Email(self.user.id).send_recovery_mail()

	def recovery_user(self):
		password = self.validated_data.get('password')
		recovery_user.delay(code_id=self.code.id, user_id=self.code.user.id, password=password)
