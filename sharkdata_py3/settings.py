"""
Django settings for sharkdata_proj project.

"""

import os
import pathlib
import logging

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Environment variables.
env_debug = os.environ.get('ENV_DJANGO_DEBUG', 'True')
env_secret_key = os.environ.get('ENV_DJANGO_SECRET_KEY', '')
env_allowed_hosts = os.environ.get('ENV_DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
env_users_and_pw = os.environ.get('ENV_DJANGO_USERS_AND_PW', 'apa:bepa,cepa:depa')
env_timezone = os.environ.get('ENV_DJANGO_TIMEZONE', 'Europe/Stockholm')
env_base_dir = os.environ.get('ENV_BASE_DIR', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if env_debug.lower() in ['true', 't', 'yes', 'y']:
    DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = pathlib.Path(BASE_DIR).parent.parent 
if env_base_dir:
    root_dir = pathlib.Path(env_base_dir)

if DEBUG:
    print('root_dir: ', root_dir)

LOGGER = logging.getLogger('SHARKdata')
SHARKDATA_DB = pathlib.Path(root_dir, 'db')
SHARKDATA_LOG = pathlib.Path(root_dir, 'log')
SHARKDATA_STATIC = pathlib.Path(root_dir, 'static')
SHARKDATA_DATA_IN = pathlib.Path(root_dir, 'data_in')
SHARKDATA_DATA = pathlib.Path(root_dir, 'data')

# Create missing directories.
if not SHARKDATA_DB.exists():
    SHARKDATA_DB.mkdir(parents=True)
if not SHARKDATA_LOG.exists():
    SHARKDATA_LOG.mkdir(parents=True)
if not SHARKDATA_STATIC.exists():
    SHARKDATA_STATIC.mkdir(parents=True)
if not SHARKDATA_DATA_IN.exists():
    SHARKDATA_DATA_IN.mkdir(parents=True)
if not SHARKDATA_DATA.exists():
    SHARKDATA_DATA.mkdir(parents=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ze+9-g*(20_*yr%+0-y(aie6u(#4y0^6g@#=962spje4lder9'
if env_secret_key:
    SECRET_KEY = env_secret_key

ALLOWED_HOSTS = ['localhost']
if env_allowed_hosts:
    host_list = []
    for host in env_allowed_hosts.split(','):
        host_list.append(host)
    ALLOWED_HOSTS = host_list

APPS_VALID_USERS_AND_PASSWORDS = {'apa': 'bepa'}
if env_users_and_pw:
    user_pw_dict = {}
    for pair in env_users_and_pw.split(','):
        user, pw = pair.split(':')
        user_pw_dict[user] = pw
    APPS_VALID_USERS_AND_PASSWORDS = user_pw_dict

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # For SHARKdata.
    
    'rest_framework_swagger',               ########### TEST. ###########
    
    'app_sharkdata_base',
    'app_datasets',
    'app_ctdprofiles',
    'app_resources',
    'app_exportformats', 
    'app_speciesobs',
    'app_sharkdataadmin',
]


########### TEST. ###########
REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }


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
        'NAME': str(pathlib.Path(SHARKDATA_DB, 'db.sqlite3')),
#         'NAME': str(pathlib.Path('/db/db.sqlite3')),
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
TIME_ZONE = env_timezone

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# Static files will be collected and put here by running the 
# command: python manage.py collectstatic
STATIC_ROOT = str(SHARKDATA_STATIC)
STATICFILES_DIRS = (
    str(pathlib.Path(BASE_DIR, 'app_sharkdata_base', 'static')), 
)

STATIC_URL = '/static/'

# Logging.
if SHARKDATA_LOG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(SHARKDATA_LOG) +'sharkdata_errors.log',
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
