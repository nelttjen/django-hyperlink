# Generated by Django 4.1.5 on 2023-02-08 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_remove_user_banned_until_remove_user_is_banned_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=50, verbose_name='Никнейм на сайте')),
                ('vk_id', models.IntegerField(default=None, null=True, verbose_name='Привязаный вк')),
                ('ban', models.JSONField(default=users.models.user_ban_json, verbose_name='Информация о бане')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Джанго юзер')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
                'db_table': 'users_profiles',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]