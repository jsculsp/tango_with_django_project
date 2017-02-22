# encoding: utf-8

import os
import sys
from jinja2.runtime import Undefined
from django_jinja.builtins import DEFAULT_EXTENSIONS

### Path Settings ###

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
sys.path.insert(1, STATIC_DIR)
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

### Core Settings ###

ALLOWED_HOSTS = ['192.168.4.134', '.linmu.date', '127.0.0.1']

## Cache ##
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        }
    }
}
REDIS_TIMEOUT = 7*24*60*60

## Database ##
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tango_with_django',
        'USER': 'root',
        'PASSWORD': 'wwg1984',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

## Debugging ##
DEBUG = True

## Email ##
ADMINS = (
    ('Mu Lin', '328232234@qq.com'),
)
EMAIL_HOST = 'smtp.qq.com'  # 'smtp.qiye.163.com'
EMAIL_HOST_PASSWORD = 'secret'
EMAIL_HOST_USER = '328232234@qq.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
SERVER_EMAIL = '328232234@qq.com'
MANAGERS = ADMINS

## File Uploads ##
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

## Globalization ##
LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

## HTTP ##
DEFAULT_CHARSET = 'utf-8'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'

## Logging ##
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'verbose': {
            'format': '%(process)d - [%(levelname)s] [%(asctime)s] - [%(pathname)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/debug.log',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
        'info_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/info.log',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/error.log',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'console_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'warning_handler': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/warning.log',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'mail_admins': {
            'include_html': True,
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['info_handler', 'error_handler', 'console_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['warning_handler'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['info_handler', 'error_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['error_handler', 'debug_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
}

## Models ##
INSTALLED_APPS = [
    # django build in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third part apps
    'registration',
    'django_jinja',
    'django_jinja.contrib._easy_thumbnails',
    'easy_thumbnails',
    'django_jinja.contrib._humanize',
    # 'django_jinja.contrib._subdomains',
    # 'subdomains',
    'django_redis',
    'redis',
    'kombu.transport.django',

    # my own apps
    'rango.apps.RangoConfig',
    'aggregation_test'
]

## Security ##
SECRET_KEY = 'dm%olv4m2tv62dhwk1vazxc92^#hhk10r7--n+s=-g*a)287bj'

## Templates ##
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'finalize': lambda x: x if x !='asdfasdfasdf' else '没有这个变量呀！',
            'match_extension': '.html',
            'match_regex': r'^(?!(admin|rango|registration|templatetags)/).*',  # This is additive to match_extension
            'app_dirname': 'templates',
            'undefined': Undefined,
            'newstyle_gettext': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'extensions': DEFAULT_EXTENSIONS + [

            ],
            'autoescape': True,
            'auto_reload': DEBUG,
            'translation_engine': 'django.utils.translation',
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    }
]

## URLs ##
ROOT_URLCONF = 'tango_with_django_project.urls'

### Auth ###
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/rango/'
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': { 'min_length': 6, },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

### Sessions ###
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600

### Site ###
SITE_ID = 1

### Static Files ###
STATIC_ROOT = "/var/www/tango_with_django_project/static/"
STATICFILES_DIRS = [STATIC_DIR, ]
STATIC_URL = '/static/'

### Others ###

# djcelery 配置
BROKER_URL = 'redis://127.0.0.1:6379/1'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_IGNORE_RESULT = True

