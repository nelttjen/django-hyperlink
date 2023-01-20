from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import ActivateCode
from users.modules import Email
from users.tasks.activate import activate_user


class ActivateSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not (code := self.initial_data.get('code', None)):
            raise ValidationError('Код не предоставлен')
        if not (code := ActivateCode.objects.filter(code__iexact=code,
                                                    is_used=False, user__is_active=False, type=1).first()):
            raise ValidationError('Код не найден или уже был использован')
        if code.expired_date < timezone.now():
            Email(code.user.id).send_activation_mail()
            code.delete()
            raise ValidationError('Код устарел. Новый код был отправлен на email, указаный при регистрации')
        return self.initial_data

    def activate(self):
        code = self.validated_data.get('code')
        activate_user.delay(code)
        return self
