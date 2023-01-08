import random
import time

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone

from django_hyperlink.settings import EMAIL_HOST_USER, DOMAIN, DEBUG
from django_hyperlink.celery import celery_app
from users.models import ActivateCode


@celery_app.task
def send_activation_code(user_id):
	if not (user := User.objects.filter(id=user_id).first()):
		return
	email = user.email
	user.save()
	if not (code := ActivateCode.objects.filter(user=user, is_used=False, expired_date__gte=timezone.now()).first()):
		code = ActivateCode(user=user).generate_code()
	send_mail(
		subject='Завершение регистрации',
		message=f'Здравствуйте! Ваша ссылка для регистрации аккаунта: {DOMAIN}/users/activate?code={code.code}. '
		        f'Ссылка действительна в течении {ActivateCode.expired_min} минут.',
		from_email=EMAIL_HOST_USER,
		recipient_list=[email, ],
		fail_silently=not DEBUG
	)
