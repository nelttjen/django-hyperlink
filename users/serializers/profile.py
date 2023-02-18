import base64
import re

from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from re import compile

from users.models import Profile, DjangoUser
from users.modules import PasswordValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ['id', 'username', 'email', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'avatar', 'title', 'bio', 'last_seen', 'rewards']


class CurrentUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'avatar', 'title', 'bio', 'last_seen', 'rewards',
                  'vk_id', 'total_redirects', 'total_redirected', 'daily_redirects', 'daily_redirected']


class UserModeratorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(max_length=10000000)
    old_password = serializers.CharField(max_length=999)
    new_password = serializers.CharField(max_length=999)
    new_password2 = serializers.CharField(max_length=999)
    unlink_vk = serializers.CharField(max_length=999)
    email = serializers.CharField(max_length=150)

    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')
        new_pass2 = data.get('new_password2')

        username = data.get('display_name')

        username_validator = compile(r'^[A-Za-zА-Яа-яёЁ0-9_-]{3,30}$')

        if old_pass and not (new_pass and new_pass2):
            raise ValidationError(_('Введите и повторите новый пароль '))

        if old_pass:
            result = PasswordValidator(new_pass, new_pass2).validate()
            if isinstance(result, str):
                raise ValidationError(_(result))

        if username and not username_validator.fullmatch(username):
            raise ValidationError('Имя пользователя должно быть 3-30 символов и '
                                  'содержать в себе только буквы латинского и русского алфавита, а также символы _-')

        return data

    def update(self, instance, data):
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')

        update_fields = []

        if old_pass and new_pass:
            if instance.user.check_password(old_pass):
                instance.user.set_password(new_pass)
                update_fields.append('password')

                del data['old_password']
                del data['new_password']
            else:
                raise ValidationError(_('Старый пароль введен неверно'))

        if mail := data.get('email'):
            instance.user.email = mail
            mail_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
            if not mail_regex.match(mail):
                raise ValidationError(_('Email указан неверно'))

            update_fields.append('email')

        if update_fields:
            instance.user.save(update_fields=update_fields)

        if data.get('avatar'):
            __, imgstr = data.get('avatar').split(';base64,')
            data['avatar'] = ContentFile(base64.b64decode(imgstr), name='temp.jpg')

        if data.get('unlink_vk'):
            instance.vk_id = None

        super().update(instance, data)

        return instance

    class Meta:
        model = Profile
        fields = ('avatar', 'old_password', 'new_password', 'new_password2', 'unlink_vk',
                  'bio', 'title', 'display_name', 'email')
