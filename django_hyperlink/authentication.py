import datetime

from django.utils import timezone
from rest_framework import authentication, exceptions


class CustomTokenAuth(authentication.TokenAuthentication):

	def authenticate_credentials(self, key):
		self.model = self.get_model()
		if not (token := self.model.objects.select_related('user').filter(key=key).first()):
			raise exceptions.AuthenticationFailed('Учетные данные не были предоставлены')

		if not token.user.is_active:
			raise exceptions.AuthenticationFailed('Пользователь неактивен')

		custom_user = token.user.user
		if custom_user.ban['is_banned']:
			msg = custom_user.ban['ban_message']
			until = custom_user.ban['ban_until']
			if until:
				if timezone.now().timestamp() < datetime.datetime.fromtimestamp(until).timestamp():
					raise exceptions.AuthenticationFailed \
						(f'Пользователь заблокирован до '
						 f'{datetime.datetime.fromtimestamp(until).strftime("%d.%m.%Y %H:%M:%S")}.'
						 f'{" Комментарий администратора: " + msg if msg else ""}')
				else:
					custom_user.ban = custom_user.ban_json
					custom_user.save()
			else:
				raise exceptions.AuthenticationFailed(f'Пользователь заблокирован навсегда.'
				                                      f'{" Комментарий администратора: " + msg if msg else ""}')
		return token.user, token
