import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone


def user_ban_json():
	return Profile.ban_json


# Create your models here.
class Profile(models.Model):
	ban_json = {
		'is_banned': False,
		'ban_until': None,
		'ban_message': None,
	}

	profile = {
		'display_name': ''
		'bio'
	}

	user = models.OneToOneField(verbose_name='Джанго юзер', to=DjangoUser, on_delete=models.CASCADE)

	display_name = models.CharField(verbose_name='Никнейм на сайте', max_length=50)
	vk_id = models.BigIntegerField(verbose_name='Привязаный вк', null=True, blank=True, default=None)

	ban = models.JSONField(verbose_name='Информация о бане', default=user_ban_json)

	class Meta:
		verbose_name = 'Профиль пользователя'
		verbose_name_plural = 'Профили пользователей'
		db_table = 'users_profiles'

	def check_ban(self):
		if self.ban['is_banned']:
			msg = self.ban['ban_message']
			until = self.ban['ban_until']
			if until:
				if timezone.now().timestamp() < datetime.datetime.fromtimestamp(until).timestamp():
					return True, f'Пользователь заблокирован до '\
					              f'{datetime.datetime.fromtimestamp(until).strftime("%d.%m.%Y %H:%M:%S")}.' \
					              f'{" Комментарий администратора: " + msg if msg else ""}'
				else:
					self.ban = user_ban_json()
					self.save()
			else:
				return True, f'Пользователь заблокирован навсегда.' \
				               f'{" Комментарий администратора: " + msg if msg else ""}'
		return False, 'збс'

	def __str__(self):
		return self.user.username


class ActivateCode(models.Model):
	expired_min = 30

	type_choises = (
		(1, 'Активация аккаунта'),
		(2, 'Восстановление пароля')
	)

	def save(self, *args, **kwargs):
		if not ActivateCode.objects.filter(id=self.pk).first():
			self.generate_code(save=False)
		super().save(*args, **kwargs)

	def generate_code(self, save=True):
		act_code = uuid.uuid4().hex[:32]
		expire = timezone.now() + datetime.timedelta(minutes=ActivateCode.expired_min)
		self.code = act_code
		self.expired_date = expire
		if save:
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


class SocialStateCodes(models.Model):
	SESSION_LIFE = 300

	owner = models.ForeignKey(verbose_name='user', to=DjangoUser, null=True, on_delete=models.CASCADE)
	state = models.CharField(verbose_name='secret code', max_length=20)
	ip = models.GenericIPAddressField(verbose_name='user ip')
	expires = models.DateTimeField(verbose_name='session')

	def is_expired(self):
		return self.expires < timezone.now()

	def set_expire(self):
		self.expires = timezone.now() + datetime.timedelta(seconds=self.SESSION_LIFE)


@receiver(signal=models.signals.post_save, sender=DjangoUser)
def user_created(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance, display_name=instance.username)
	instance.user.save()