from rest_framework import authentication, exceptions


class CustomTokenAuth(authentication.TokenAuthentication):

	def authenticate_credentials(self, key):
		self.model = self.get_model()
		if not (token := self.model.objects.select_related('user').filter(key=key).first()):
			raise exceptions.AuthenticationFailed('Учетные данные не были предоставлены.')

		if not token.user.is_active:
			raise exceptions.AuthenticationFailed('Пользователь неактивен')

		custom_user = token.user.user
		result, msg = custom_user.check_ban()
		if result:
			raise exceptions.AuthenticationFailed(msg)
		return token.user, token
