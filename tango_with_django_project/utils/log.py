import time


def log(*args, **kwargs):
    f = '%Y/%m%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    with open('log.txt', 'a') as f:
        print('============================================', file=f)
        print(dt, *args, file=f, **kwargs)
        print('============================================', file=f)
        print('', file=f)