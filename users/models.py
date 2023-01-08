import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone


# Create your models here.
class User(models.Model):
	user = models.OneToOneField(verbose_name='Джанго юзер', to=DjangoUser, on_delete=models.CASCADE)


class ActivateCode(models.Model):
	expired_min = 30

	def generate_code(self):
		act_code = uuid.uuid4().hex[:32]
		expire = timezone.now() + datetime.timedelta(minutes=ActivateCode.expired_min)
		self.code = act_code
		self.expired_date = expire
		self.save()
		return self

	user = models.ForeignKey(verbose_name='Юзер', to=DjangoUser, on_delete=models.CASCADE)
	code = models.CharField(verbose_name='Код активации', max_length=32, unique=True)
	is_used = models.BooleanField(verbose_name='Использован?', default=False)
	expired_date = models.DateTimeField(verbose_name='Срок годности')


@receiver(signal=models.signals.post_save, sender=DjangoUser)
def user_created(sender, instance, created, **kwargs):
	if created:
		User.objects.create(user=instance)
	instance.user.save()