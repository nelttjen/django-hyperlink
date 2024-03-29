# Generated by Django 4.1.5 on 2023-02-09 21:47

from django.db import migrations, models
import django_hyperlink.modules.storage


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_daily_redirected_profile_daily_redirects_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRewards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('rank', models.IntegerField(choices=[(0, 'Стандартная'), (1, 'Серебрянная'), (2, 'Золотая'), (3, 'Платиновая')], default=0, verbose_name='Ранг')),
                ('image', models.ImageField(upload_to=django_hyperlink.modules.storage.MediaStorage(), verbose_name='Иконка')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/static/default/img/no-avatar.jpg', upload_to=django_hyperlink.modules.storage.MediaStorage(), verbose_name='Аватар'),
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Заголовок профиля'),
        ),
        migrations.AddField(
            model_name='usernotifications',
            name='is_viewed',
            field=models.BooleanField(default=False, verbose_name='Просмотрено?'),
        ),
    ]
