from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShareLink(models.Model):
    redirect_time_choices = (
        (0, 'Моментально'),
        (3, '3 секунды'),
        (5, '5 секунд'),
        (10, '10 секунд'),
        (15, '15 секунд'),
    )

    owner = models.ForeignKey(verbose_name='Владелец', to=User, on_delete=models.CASCADE, default=None, null=True)
    share_code = models.CharField(verbose_name='Код', max_length=30)
    redirect_timer = models.PositiveIntegerField(verbose_name='Время до редиректа', default=5, choices=redirect_time_choices)
    redirect_to = models.URLField(verbose_name='Куда ведет ссылка')
    valid_until = models.DateTimeField(verbose_name='Истекает', null=True, default=None)
    allowed_redirects = models.IntegerField(verbose_name='Максимум редиректов', default=-1)
    redirects = models.IntegerField(verbose_name='Количество редиректов', default=0)
    date_created = models.DateTimeField(verbose_name='Дата созания', auto_now_add=True)
    only_unique_redirects = models.BooleanField(verbose_name='Считать только уникальные переходы?', default=False)
    is_active = models.BooleanField(verbose_name='Активная?', default=True)

    class Meta:
        db_table = 'share_links'
        verbose_name = 'Сокращенная ссылка'
        verbose_name_plural = 'Сокращенные ссылки'

    def __str__(self):
        return f'Ссылка {self.share_code} (id{self.id})'


class LinkRedirect(models.Model):
    link = models.ForeignKey(verbose_name='Ссылка', to='link.ShareLink', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(verbose_name='Кто перешел', to=User, on_delete=models.CASCADE, null=True, default=None)
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес', null=True, default=None)
    date = models.DateTimeField(verbose_name='Дата перехода', auto_now_add=True)