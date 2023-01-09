import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone


# Create your models here.
class User(models.Model):
	user = models.OneToOneField(verbose_name='Джанго юзер', to=DjangoUser, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'
		db_table = 'custom_users'

	def __str__(self):
		return self.user.username


class ActivateCode(models.Model):
	expired_min = 30

	type_choises = (
		(1, 'Активация аккаунта'),
		(2, 'Восстановление пароля')
	)

	def generate_code(self):
		act_code = uuid.uuid4().hex[:32]
		expire = timezone.now() + datetime.timedelta(minutes=ActivateCode.expired_min)
		self.code = act_code
		self.expired_date = expire
		self.save()
		return self

	user = models.ForeignKey(verbose_name='Юзер', to=DjangoUser, on_delete=models.CASCADE)
	code = models.CharField(verbose_name='Код активации', max_length=32, unique=True)
	type = models.IntegerField(verbose_name='Тип кода', choices=type_choises)
	is_used = models.BooleanField(verbose_name='Использован?', default=False)
	expired_date = models.DateTimeField(verbose_name='Срок годности')
	activated_date = models.DateTimeField(verbose_name='Дата активации', null=True, default=None)

	class Meta:
		verbose_name = 'Код пользователя'
		verbose_name_plural = 'Коды пользователя'
		db_table = 'user_codes'

	def __str__(self):
		return f'Код пользователя {self.user.username}'


@receiver(signal=models.signals.post_save, sender=DjangoUser)
def user_created(sender, instance, created, **kwargs):
	if created:
		User.objects.create(user=instance)
	instance.user.save()