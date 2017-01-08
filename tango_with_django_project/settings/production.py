from .develop import *

DEBUG = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_HSTS_SECONDS = 60
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True


SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = 'https://static.linmu.date/static/'
MEDIA_URL = 'https://static.linmu.date/media/'

DATABASES['default']['PASSWORD'] = 'root'
DATABASES['default']['USER'] = 'root'