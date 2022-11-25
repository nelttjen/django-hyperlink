from celery import Celery


celery_app = Celery('django_hyperlink')
celery_app.config_from_object()
celery_app.autodiscover_tasks()