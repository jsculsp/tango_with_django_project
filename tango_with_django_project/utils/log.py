import time
from pprint import pprint


def log(*args, **kwargs):
    f = '%Y/%m%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    with open('log.txt', 'a') as f:
        print('============================================', file=f)
        print(dt, *args, file=f, **kwargs)
        print('============================================', file=f)


def plog(obj):
    with open('log.txt', 'a') as f:
        print('============================================', file=f)
        pprint(obj, stream=f)
        print('============================================', file=f)
        print('', file=f)