from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone

from django_hyperlink.settings import EMAIL_HOST_USER, DEBUG
from django_hyperlink.celery import celery_app
from users.models import ActivateCode


@celery_app.task
def send_activation_code(email, subject, message):
	if isinstance(message, list):
		message = message[0]
	send_mail(
		subject=subject,
		message=message,
		from_email=EMAIL_HOST_USER,
		recipient_list=[email, ],
		fail_silently=not DEBUG
	)


@celery_app.task
def recovery_user(code_id, user_id, password):
	ActivateCode.objects.filter(id=code_id).update(
		is_used=True,
		activated_date=timezone.now()
	)
	user = User.objects.filter(id=user_id).first()
	user.set_password(password)
	user.save()