import datetime

from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from users.models import ActivateCode
from users.modules import Email
from users.tasks.user_code import send_activation_code
from users.tasks.activate import activate_user


class LoginSerializer(serializers.Serializer):

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super().__init__(*args, **kwargs)

	def validate(self, attrs):
		if (username := self.initial_data.get('username')) and (password := self.initial_data.get('password')):
			self.user = User.objects.filter(
				Q(username=username) | Q(email=username)
			).first()
			if not self.user:
				raise ValidationError(_('Неверный логин или пароль'))
			if not self.user.check_password(password):
				raise ValidationError(_('Неверный логин или пароль'))
			if not self.user.is_active:
				raise ValidationError(_('На вашу почту было выслано письмо с кодом подтверждения'))
		else:
			raise ValidationError(_('Неверный логин или пароль'))
		ban, msg = self.user.user.check_ban()
		if ban:
			raise ValidationError(_(msg))
		return self.initial_data

	def login(self):
		user = self.user
		token, created = Token.objects.get_or_create(user=user)
		username = self.user.username
		return {'token': token.key, 'username': username}
