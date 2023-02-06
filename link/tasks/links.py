from django.db.models import F, Q

from django_hyperlink.celery import celery_app
from link.models import ShareLink, LinkRedirect

import logging


@celery_app.task
def update_link_redirects(link_id, user_id, ip=None, is_unique=False):
    if not link_id:
        logging.warning(f'update_link_redirects got an empty link_id: {link_id}')
        return False

    if is_unique:
        filt = Q(ip_address=ip) & Q(ip_address__isnull=False)

        if user_id:
            filt = Q(user_id=user_id) & Q(user_id__isnull=False)

        exists = LinkRedirect.objects.filter(filt).exists()
        update = not exists
    else:
        exists = False
        update = True

    if update:
        ShareLink.objects.filter(id=link_id).update(
            redirects=F('redirects') + 1
        )

    if not exists:
        LinkRedirect.objects.create(
            link_id=link_id,
            user_id=user_id,
            ip_address=ip,
        )

