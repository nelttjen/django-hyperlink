from django.utils.encoding import filepath_to_uri
from datetime import datetime, timedelta
from urllib.parse import urlencode
from storages.backends.s3boto3 import S3Boto3Storage

from django_hyperlink.settings import STORAGE_BUCKET_NAME


class MediaStorage(S3Boto3Storage):
    bucket_name = STORAGE_BUCKET_NAME
    location = 'media'


class StaticStorage(S3Boto3Storage):
    bucket_name = STORAGE_BUCKET_NAME
    location = 'static'


MEDIA_STORAGE = MediaStorage()
STATIC_STORAGE = StaticStorage()