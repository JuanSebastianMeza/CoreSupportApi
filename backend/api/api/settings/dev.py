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


JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'api.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'api.utils.jwt_get_username_from_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,

    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=5),

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=2),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_db',
        'USER': 'solucionesagiles',
        'PASSWORD': 'canaima123++',
        'HOST': '172.31.158.5',
        'PORT': '3306',
    }
}
