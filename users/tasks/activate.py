from django.utils import timezone

from django_hyperlink.celery import celery_app
from users.models import ActivateCode


@celery_app.task
def activate_user(code):
	code = ActivateCode.objects.filter(code__iexact=code).select_related('user').first()
	code.user.is_active = True
	code.user.save()

	code.is_used = True
	code.activated_date = timezone.now()
	code.save()
