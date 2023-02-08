from re import compile

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError

from users.modules import Email, PasswordValidator


class RegisterSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = (
			'username',
			'email',
		)

		extra_kwargs = {'password': {'write_only': True}}

	def validate(self, args):
		username = self.initial_data.get('username')
		email = self.initial_data.get('email')
		password = self.initial_data.get('password')
		password_again = self.initial_data.get('password_again')
		username_validator = compile(r'^[A-Za-z0-9_-]{3,20}$')
		password_validator = PasswordValidator(password, password_again)
		if not all([username, email, password, password_again]):
			raise ValidationError('Не хватает аргументов')
		if not username_validator.fullmatch(username):
			raise ValidationError('Имя пользователя должно быть 3-20 символов и '
			                      'содержать в себе только буквы латинского алфавита, а также символы _-')
		if isinstance(error := password_validator.validate(), str):
			raise ValidationError(error)
		if User.objects.filter(username__iexact=username).first():
			raise ValidationError('Имя пользователя уже занято')
		if User.objects.filter(email__iexact=email).first():
			raise ValidationError('Email уже используется')
		return self.initial_data

	def create(self, validated_data):
		username = validated_data.get('username')
		password = validated_data.get('password')
		email = validated_data.get('email')
		user = User.objects.create_user(
			username=username,
			password=password,
			email=email
		)
		user.is_active = False
		user.save()
		Email(user.id).send_activation_mail()
		return user
