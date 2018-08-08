"""
Django test settings
"""
from .base import * # pylint: disable=wildcard-import, unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

CORS_ORIGIN_ALLOW_ALL = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['AUTH_DB_NAME'],
        'USER': os.environ['AUTH_DB_USER'],
        'PASSWORD': os.environ['AUTH_DB_PASS'],
        'HOST': os.environ['AUTH_DB_HOST'],
        'PORT': os.environ['AUTH_DB_PORT'],
    }
}
