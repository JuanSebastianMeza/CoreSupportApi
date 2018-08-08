"""
Django prod settings
"""
from .base import * # pylint: disable=wildcard-import, unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get('APP_HOSTNAME')]

# INSTALLED_APPS += [
# 	'',
# ]

# Add static root
STATIC_ROOT = os.path.join(MAIN_DIR, 'static_root')

# Add media_root
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(MAIN_DIR, 'media_root')

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
