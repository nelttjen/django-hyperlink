from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers.profile import CurrentUserProfileSerializer
from users.modules import Auth


class LoginSerializer(serializers.Serializer):

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request')
		super().__init__(*args, **kwargs)

	def validate(self, attrs):
		self.auth = Auth()
		result = self.auth.authenticate_user(self.initial_data.get('username'), self.initial_data.get('password'))

		if isinstance(result, str):
			raise ValidationError(_(result))

		return self.initial_data

	def login(self, request):
		self.auth.request = request
		token = self.auth.authenticate()
		return {'token': token, 'profile': CurrentUserProfileSerializer(self.auth.user.profile).data}
