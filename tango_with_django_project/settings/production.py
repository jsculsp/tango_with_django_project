from .develop import *

DEBUG = True

STATIC_URL = 'https://static.linmu.date/static/'
MEDIA_URL = 'https://static.linmu.date/media/'

DATABASES['default']['PASSWORD'] = 'root'
DATABASES['default']['USER'] = 'root'