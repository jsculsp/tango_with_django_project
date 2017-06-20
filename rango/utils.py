import json

from django.conf import settings
from django.core.cache import cache


# read cache user id
def read_from_cache(user_name):
    key = 'user_id_of_{}'.format(user_name)
    value = cache.get(key)
    if value is None:
        data = None
    else:
        data = json.loads(value)
    return data


# write cache user id
def write_to_cache(user_name, value):
    key = 'user_id_of_{}'.format(user_name)
    cache.set(key, json.dumps(value), settings.REDIS_TIMEOUT)
