"""
Django dev settings
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
SECRET_KEY = 'q4u$ueupa_5$zry3mmh6aqn@g^-4k-(1-bbfr6do(f7%e$aok!'


# # Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_db',
        'USER': 'solucionesagiles',
        'PASSWORD': 'canaima123++',
        'HOST': '10.64.9.49',
        'PORT': '3306',
    }
}
