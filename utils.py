import time
from pprint import pprint


def log(*args, **kwargs):
    f = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    with open('logs/log.txt', 'a', encoding='utf-8') as file:
        print('============================================', file=file)
        print(dt, *args, file=file, **kwargs)
        print('============================================', file=file)
        print('', file=file)


def plog(obj):
    with open('logs/log.txt', 'a') as file:
        print('============================================', file=file)
        pprint(obj, stream=file)
        print('============================================', file=file)
        print('', file=file)
