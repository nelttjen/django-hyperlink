from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone

from django_hyperlink.settings import EMAIL_HOST_USER, DOMAIN, DEBUG
from django_hyperlink.celery import celery_app
from users.models import ActivateCode


@celery_app.task
def send_activation_code(code, email):
	send_mail(
		subject='Завершение регистрации',
		message=f'Здравствуйте! Ваша ссылка для регистрации аккаунта: {DOMAIN}/users/activate/?code={code}. '
		        f'Ссылка действительна в течении {ActivateCode.expired_min} минут. Код для активации: {code}',
		from_email=EMAIL_HOST_USER,
		recipient_list=[email, ],
		fail_silently=not DEBUG
	)
