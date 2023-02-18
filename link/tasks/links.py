from django.db.models import F, Q

from celery import shared_task
from django_hyperlink.celery import celery_app
from link.models import ShareLink, LinkRedirect
from users.models import Profile

import logging


@celery_app.task
def update_link_redirects(link_id, user_id, ip=None, is_unique=False):
    if not link_id:
        logging.warning(f'update_link_redirects got an empty link_id: {link_id}')
        return False
    link = ShareLink.objects.filter(id=link_id).first()

    if is_unique:
        filt = (Q(ip_address=ip) & Q(ip_address__isnull=False)) & Q(link_id=link_id)

        if user_id:
            filt = ((Q(ip_address=ip) & Q(ip_address__isnull=False)) |
                    (Q(user_id=user_id) & Q(user_id__isnull=False))) & Q(link_id=link_id)

        queryset = LinkRedirect.objects.filter(filt)
        if user_id:
            redirect = queryset.first()
            if redirect.ip_address and not redirect.user_id:
                queryset.select_for_update().update(user_id=user_id)
            exists = redirect
        else:
            exists = queryset.exists()

        update = not exists
    else:
        exists = False
        update = True

    if update:
        ShareLink.objects.filter(id=link_id).update(
            redirects=F('redirects') + 1
        )
        Profile.objects.filter(user_id=user_id).update(
            daily_redirects=F('daily_redirects') + 1,
            total_redirects=F('total_redirects') + 1,
        )
        if link:
            Profile.objects.filter(user_id=link.owner_id)

    if not exists:
        LinkRedirect.objects.create(
            link_id=link_id,
            user_id=user_id,
            ip_address=ip,
        )


@shared_task
def daily_refresh(*args):
    Profile.objects.filter(Q(daily_redirects__gt=0) | Q(daily_redirected__gt=0)).update(
        daily_redirects=0,
        daily_redirected=0
    )
    Profile.objects.bulk_update()