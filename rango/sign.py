#coding: UTF-8
'''
Created on 2013-10-14

@author: butter
'''
import copy
import hashlib
import time


def make_source(params):
    '''
    根据参数字典生成排序的源签名串
    params: 参数字典
    '''
    for k in params.keys():
        if (type(params[k]) == str):
            continue
        elif type(params[k]) == int:
            params[k] = str(params[k])
        else:
            raise Exception('illegal params value type %s(%s).' %(k, type(params[k])))
    keys = sorted(params.keys())
    list_params = map(lambda it: '%s=%s' % (it.encode('utf-8'), params[it]), keys)
    str_params = '&'.join(list_params)
    return str_params

def make_sign(params, key, **kargs):
    '''
    对参数字典生成签名
    params: 参数字典
    key: 签名秘钥
    kargs: only, defer
    '''
    params = copy.deepcopy(params)
    sign_keys = set(params.keys())
    if 'only' in kargs and kargs['only']:
        sign_keys = set(params.keys()) & set(kargs['only'])
    elif 'defer' in kargs and kargs['defer']:
        sign_keys = set(params.keys()) - set(kargs['defer'])

    tmp_params = {}
    for k in sign_keys:
        tmp_params[k] = params[k]
    params = tmp_params

    params['key'] = key
    sign_source = make_source(params)
    return hashlib.md5(sign_source.encode('utf-8')).hexdigest()

def verify_sign(params, key, sign, **kwargs):
    '''
    验证签名是否正确
    params: 参数字典
    key: 密钥
    sign: 签名
    kargs: only, defer
    '''
    return make_sign(params, key, **kwargs)==sign

def make_timestamp():
    '''
    生成系统时间戳
    '''
    return str(int(time.time()))

def verify_timestamp(timestamp, term=60, deviation=60):
    '''
    验证时间戳是否有效
    timestamp: 时间戳(s)
    term: 签名有效时间(s)
    deviation: 签名系统跟验签系统时间误差(s)
    '''
    cur_timestamp = int(make_timestamp())
    timestamp = int(timestamp)
    return (timestamp >= (cur_timestamp-term-deviation)) and (timestamp <= (cur_timestamp+deviation))