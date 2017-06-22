import copy
import json
from functools import wraps
from xml.etree import cElementTree as ET
import hashlib
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tango_with_django_project.utils.log import log, plog

WEPAY_APIKEY = u"ffa02b3acd6c11e68cc600163e003d10"
with open('alipay_public') as f:
    verify_key = RSA.importKey(f.read())
verifier = Signature_pkcs1_v1_5.new(None)


def verify_async_signature(**kwargs):
    sign = kwargs[u"sign"]
    arguments = [(key, val) for (key, val) in kwargs.items() if val and key != u"sign" and key != u"sign_type"]
    arguments.sort(key=lambda p: p[0])
    log('arguments: ', arguments)
    data = u""
    for (key, val) in arguments:
        data += key + u"=" + val + u"&"
    data = data[:-1]
    return __verify_ras2_signature(data, sign)


def __verify_ras2_signature(data, sign):
    data = data.encode('utf-8')
    digest = SHA256.new()
    digest.update(data)
    return verifier.verify(digest, base64.b64decode(sign))


def get_md5_signature(**kwargs):
    arguments = [(key, val) for (key, val) in kwargs.items() if val and key != u"sign"]
    arguments.sort(key=lambda p: p[0])
    data = u""
    for (key, val) in arguments:
        data += key + u"=" + val + u"&"
    data += u"key=" + WEPAY_APIKEY
    md5 = hashlib.md5()
    md5.update(data.encode())
    return md5.hexdigest().upper()


def verify_wechat_signature(view_func):
    """
    校验微信签名
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        content = """
            <xml>
                <return_code><![CDATA[{0}]]></return_code>
                <return_msg><![CDATA[{1}]]></return_msg>
            </xml>
        """
        # 验证签名是否正确
        body = request.body
        root = ET.fromstring(body)
        params = dict()
        for child in root:
            params[child.tag] = child.text
        request.params = copy.deepcopy(params)
        param_sign = params['sign']
        local_sign = get_md5_signature(**params)
        if local_sign != param_sign:
            content = content.format('FAIL', 'NOT OK')
            log('debug location xixihaha')
            return HttpResponse(content, content_type="application/xml")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def verify_alipay_signature(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        params = request.POST.dict()
        plog(params)
        if verify_async_signature(**params):
            log('debug location 0...')
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('fail')
    return wrapped_view


@csrf_exempt
@verify_wechat_signature
def fcoin_order_notify_wepay(request):
    content = """
                <xml>
                    <return_code><![CDATA[{0}]]></return_code>
                    <return_msg><![CDATA[{1}]]></return_msg>
                </xml>
            """
    result_code = request.params['result_code']
    if result_code != 'SUCCESS':
        content = content.format('FAIL', 'NOT OK')
        return HttpResponse(content, content_type='application/xml')
    out_trade_no = request.params['out_trade_no']
    log('out_trade_no: ', out_trade_no)
    content = content.format('SUCCESS', 'OK')
    return HttpResponse(content, content_type='application/xml')


@csrf_exempt
@verify_alipay_signature
def fcoin_order_notify_alipay(request):
    log('success!!!')
    return HttpResponse('success')
