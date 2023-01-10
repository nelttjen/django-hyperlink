import copy
from re import compile

from django.contrib.auth.models import User as DjangoUser
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.authtoken.admin import User as RestUser
from rest_framework.serializers import ModelSerializer, ValidationError

from django_hyperlink.public_settings import DOMAIN
from django_hyperlink.settings import EMAIL_HOST_USER
from users.models import ActivateCode
from users.tasks.user_code import send_activation_code
from users.modules import Email

class RegisterSerializer(ModelSerializer):
	class Meta:
		model = RestUser
		fields = (
			'username',
			'email',
			'password',
		)
		# optional_fields = ()

		extra_kwargs = {'password': {'write_only': True, 'validators': None}, 'username': {'validators': None}}

	def validate(self, args):
		username = self.initial_data.get('username')
		email = self.initial_data.get('email')
		password = self.initial_data.get('password')
		password_again = self.initial_data.get('password_again')
		username_validator = compile(r'^[A-Za-z0-9_-]{3,20}$')
		password_validator = compile(r'^[A-Za-z0-9_#@$&*-]{3,50}$')
		if not all([username, email, password, password_again]):
			raise ValidationError('Не хватает аргументов')
		if not username_validator.fullmatch(username):
			raise ValidationError('Имя пользователя должно быть 3-20 символов и '
			                      'содержать в себе только буквы латинского алфавита, а также символы _-')
		if not password_validator.fullmatch(password):
			raise ValidationError('Пароль должен быть 3-50 символов и '
			                      'содержать в себе только буквы латинского алфавита, а также символы _#@$&*-')
		if password != password_again:
			raise ValidationError('Пароли не совпадают')
		if DjangoUser.objects.filter(username__iexact=username).first():
			raise ValidationError('Имя пользователя уже занято')
		if DjangoUser.objects.filter(email__iexact=email).first():
			raise ValidationError('Email уже используется')
		return self.initial_data

	def create(self, validated_data):
		username = validated_data.get('username')
		password = validated_data.get('password')
		email = validated_data.get('email')
		user = DjangoUser.objects.create_user(
			username=username,
			password=password,
			email=email
		)
		user.is_active = False
		user.save()
		Email(user.id).send_activation_mail()
		return user
