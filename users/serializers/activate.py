import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import ActivateCode
from users.tasks.user_code import send_activation_code
from users.tasks.activate import activate_user


class ActivateSerializer(serializers.Serializer):
	def validate(self, attrs):
		if not (code := self.initial_data.get('code', None)):
			raise ValidationError('Код не предоставлен')
		if not (code := ActivateCode.objects.filter(code__iexact=code,
		                                            is_used=False, user__is_active=False, type=1).first()):
			raise ValidationError('Код не найден или уже был использован')
		if code.expired_date < timezone.now():
			send_activation_code.delay(user_id=code.user.id)
			code.delete()
			raise ValidationError('Код устарел. Новый код был отправлен на email, указаный при регистрации')
		return self.initial_data

	def activate(self):
		code = self.validated_data.get('code')
		activate_user.delay(code)
		return self
