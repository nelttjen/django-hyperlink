celery -A django_hyperlink.celery_app worker -P solo --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair