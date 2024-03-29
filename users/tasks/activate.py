from django.utils import timezone

from django_hyperlink.celery import celery_app
from users.models import ActivateCode

import logging


@celery_app.task
def activate_user(code):
    code = ActivateCode.objects.filter(code=code).select_related('user').first()

    try:
        code.user.is_active = True
        code.user.save()

        code.is_used = True
        code.activated_date = timezone.now()
        code.save()
    except:
        logging.error(f'Activate: Code {code} was not found')
        return False

    return True
