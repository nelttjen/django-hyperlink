import datetime
import os
import uuid

from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone
from django_hyperlink.modules.storage import MEDIA_STORAGE
from django_hyperlink.settings import MEDIA_URL
from oauth2_provider.models import AccessToken


def user_ban_json():
    return Profile.ban_json


# Create your models here.
class Profile(models.Model):
    ban_json = {
        'is_banned': False,
        'ban_until': None,
        'ban_message': None,
    }

    def get_file_path(self, filename):
        filename = f'{self.pk}/avatar_{uuid.uuid4().hex[:8]}.jpg'
        return os.path.join('users', filename)

    def get_avatar_link(self):
        return f'{MEDIA_URL}{self.avatar.name}'

    user = models.OneToOneField(verbose_name='Джанго юзер', to=DjangoUser, on_delete=models.CASCADE)

    # main
    display_name = models.CharField(verbose_name='Никнейм на сайте', max_length=50, db_index=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to=get_file_path, default='static/default/img/no-avatar.jpg')
    title = models.CharField(verbose_name='Заголовок профиля', max_length=150, blank=True)
    bio = models.TextField(verbose_name='О себе', blank=True)

    # moderation
    last_seen = models.DateTimeField(verbose_name='Последний раз в сети')
    last_ip = models.GenericIPAddressField(verbose_name='Последний IP адрес')
    ban = models.JSONField(verbose_name='Информация о бане', default=user_ban_json)

    # socials
    vk_id = models.BigIntegerField(verbose_name='Привязаный вк', null=True, blank=True, default=None, unique=True, db_index=True)

    # statistics
    total_redirects = models.PositiveIntegerField(verbose_name='Кол-во переходов по ссылкам', default=0)
    total_redirected = models.PositiveIntegerField(verbose_name='Кол-во переходов пользователей по ссылкам', default=0)

    daily_redirects = models.PositiveIntegerField(verbose_name='Кол-во переходов по ссылкам за день', default=0)
    daily_redirected = models.PositiveIntegerField(verbose_name='Кол-во переходов пользователей по ссылкам за день', default=0)

    # other
    rewards = models.ManyToManyField(verbose_name='Награды', to='users.UserRewards', blank=True)

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
                    return True, f'Пользователь заблокирован до ' \
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
        return f'{self.display_name} ({self.user.username})'

    def delete_avatars(self):
        storage = MEDIA_STORAGE

        exists_images = storage.listdir(f'users/{self.pk}/')[1]
        for image in exists_images:
            if image.endswith('.jpg') and image.startswith(f'avatar_'):
                storage.delete(os.path.join(f'users/{self.pk}/', image))

    def save(self, *args, **kwargs):
        storage = MEDIA_STORAGE

        method = 'update'
        profile = Profile.objects.filter(id=self.pk).first()

        if not profile:
            method = 'create'

        super().save(*args, **kwargs)

        if self.ban['is_banned']:
            AccessToken.objects.filter(user_id=self.user_id).delete()

        if method == 'update':
            if profile.avatar.name != self.avatar.name:
                im = Image.open(storage.open(self.avatar.name))
                im = im.convert('RGB')
                im = im.resize((128, 128))
                img_buffer = BytesIO()
                im.save(img_buffer, 'JPEG', quality=100, optimize=True, progressive=True)

                self.delete_avatars()

                storage.save(self.avatar.name, ContentFile(img_buffer.getvalue()))

                img_buffer.close()
                im.close()
            elif not self.avatar:
                self.delete_avatars()


class UserNotifications(models.Model):
    actions = (
        (0, 'Переадресация'),
        (1, 'Подтверждение'),
    )

    profile = models.ForeignKey(verbose_name='Пользователь', to='users.Profile', on_delete=models.CASCADE)

    title = models.CharField(verbose_name='Заголовок оповещения', max_length=100)
    text = models.TextField(verbose_name='Текст оповещения', blank=True)

    action = models.IntegerField(verbose_name='Тип действия', default=0, choices=actions)
    action_content = models.CharField(verbose_name='Контент действия', max_length=999, blank=True)

    is_viewed = models.BooleanField(verbose_name='Просмотрено?', default=False)


class UserRewards(models.Model):
    ranks = (
        (0, 'Стандартная'),
        (1, 'Серебрянная'),
        (2, 'Золотая'),
        (3, 'Платиновая')
    )

    name = models.CharField(verbose_name='Название', max_length=100)
    rank = models.IntegerField(verbose_name='Ранг', choices=ranks, default=0)
    image = models.ImageField(verbose_name='Иконка', upload_to=MEDIA_STORAGE)


class UserHistory(models.Model):
    profile = models.ForeignKey(verbose_name='Профиль', to='users.Profile', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='Айпи', db_index=True)
    count = models.IntegerField(verbose_name='Кол-во входов', default=0)


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
    instance.profile.save()