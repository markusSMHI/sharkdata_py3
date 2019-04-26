"""
Django settings for sharkdata_proj project.
For Django 2.2 and Python 3.
Source code: 

For SHARKdata:
- Copy this file (TEMPLATE_settings.py) to sharkdata_proj/sharkdata_proj/settings.py
- Replace all '<REPLACE>' with proper values.
- Don't use "DEBUG = True" in production.
"""

import os
import pathlib
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ze+9-g*(20_*yr%+0-y(aie6u(#4y0^6g@#=962spje4lder9'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False # <REPLACE>
DEBUG = True # <REPLACE>

ALLOWED_HOSTS = ['localhost', '<REPLACE>']


# Application specific constants.
parent_dir = pathlib.Path(BASE_DIR).parent.parent
LOGGER = logging.getLogger('SHARKdata')
LOGGING_PATH = pathlib.Path(parent_dir, 'sharkdata_log')
SHARKDATA_DATA_IN = pathlib.Path(parent_dir, 'data_in')
SHARKDATA_DATA = pathlib.Path(parent_dir, 'data')
APPS_VALID_USERS_AND_PASSWORDS_FOR_TEST = {'apa': 'bepa'}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # For SHARKdata.
    'app_sharkdata_base',
    'app_datasets',
    'app_ctdprofiles',
    'app_resources',
    'app_exportformats', 
    'app_speciesobs',
    'app_sharkdataadmin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sharkdata_py3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sharkdata_py3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(pathlib.Path(SHARKDATA_DATA, 'db', 'db.sqlite3')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# Static files will be collected and put here by running the 
# command: python manage.py collectstatic
STATIC_ROOT = str(pathlib.Path(SHARKDATA_DATA, 'static'))
STATICFILES_DIRS = (
    str(pathlib.Path(BASE_DIR, 'app_sharkdata_base', 'static')), 
)

STATIC_URL = '/static/'


# Logging.
if LOGGING_PATH:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(LOGGING_PATH) +'sharkdata_errors.log',
                'maxBytes': 1024*1024,
                'backupCount': 10,
            },
        },
        'loggers': {
            '': {
                'handlers': ['file_error'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
