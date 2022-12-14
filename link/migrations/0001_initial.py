# Generated by Django 4.1.3 on 2022-11-25 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_code', models.CharField(max_length=30)),
                ('redirect_timer', models.IntegerField(default=5)),
                ('redirect_to', models.URLField()),
                ('valid_until', models.DateTimeField()),
                ('allowed_redirects', models.IntegerField(default=-1)),
                ('redirects', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_sharable', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
