import os
from celery import Celery
from django_hyperlink.settings import INSTALLED_APPS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_hyperlink.settings')

celery_app = Celery('django_hyperlink')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: INSTALLED_APPS)
