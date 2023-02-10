"""
Django settings for django_hyperlink project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = load_dotenv(BASE_DIR / 'django_hyperlink/.env')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'storages',

    'oauth2_provider',

    # Apps
    'link.apps.LinkConfig',
    'users.apps.UsersConfig',

    # API app
    'api.v1.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django_hyperlink.middleware.OAuth2TokenMiddleware',
    'django_hyperlink.middleware.CheckAuthMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django_hyperlink.backends.APIAuth',
]

LOGOUT_REDIRECT_URL = '/users/logout/'

# REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'django_hyperlink.backends.OAuth2Authentication',
        'django_hyperlink.backends.APIAuth',
    ],
    'EXCEPTION_HANDLER': 'django_hyperlink.exceptions.custom_exception_handler',
}

# OAUTH
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 2592000,
    'SCOPES': {'all': 'all'},
}
OAUTH2_DEFAULT_APP = 1


# Social
SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get('VK_KEY', '')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('VK_SECRET', '')

ROOT_URLCONF = 'django_hyperlink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'link/templates',
            BASE_DIR / 'users/templates',

            BASE_DIR / 'templates',
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_hyperlink.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "postgres",
        "USER": os.environ.get('POSTGRES_DB', 'postgres'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        "HOST": os.environ.get('POSTGRES_HOST', 'localhost'),
        "PORT": os.environ.get('POSTGRES_PORT', 5432)
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DOMAIN
DOMAIN = 'http://127.0.0.1:8000'

# api
API_PATH = 'api/v1/'
API_FOLDER = 'api.v1.urls'

# celery
REDIS_HOST = 'redis'
REDIS_PORT = 6379
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587


# DRF_YASG
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'None': {
            'type': None
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization: Token <token>',
            'in': 'header'
        }
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'dj-hyperlink-bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
}
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'django_hyperlink.modules.storage.MediaStorage'
