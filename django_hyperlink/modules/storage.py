from storages.backends.s3boto3 import S3Boto3Storage

from django_hyperlink.settings import AWS_STORAGE_BUCKET_NAME


class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = AWS_STORAGE_BUCKET_NAME


class StaticStorage(S3Boto3Storage):
    location = 'static'
    bucket_name = AWS_STORAGE_BUCKET_NAME


MEDIA_STORAGE = MediaStorage()
STATIC_STORAGE = StaticStorage()