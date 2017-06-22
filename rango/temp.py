import copy
import json
from functools import wraps
from xml.etree import cElementTree as ET

from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rango import sign
from tango_with_django_project.utils.log import log, plog

WEPAY_APIKEY = u"ffa02b3acd6c11e68cc600163e003d10"


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
        # try:
        # 验证签名是否正确
        body = request.body
        root = ET.fromstring(body)
        params = dict()
        for child in root:
            params[child.tag] = child.text
        request.params = copy.deepcopy(params)
        param_sign = params['sign']
        del params['sign']
        if not sign.verify_sign(params, WEPAY_APIKEY, param_sign):
            content = content.format('FAIL', 'NOT OK')
            log('debug location xixihaha')
            return HttpResponse(content, mimetype="application/xml")
        # except:
        #     content = content.format('FAIL', 'NOT OK')
        #     return HttpResponse(content, mimetype="application/xml")

        return view_func(request, *args, **kwargs)

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
    result_code = request.POST['result_code']
    if result_code != 'SUCCESS':
        content = content.format('FAIL', 'NOT OK')
        return HttpResponse(content, content_type='application/xml')
    out_trade_no = request.POST['out_trade_no']

    content = content.format('SUCCESS', 'OK')
    return HttpResponse(content, content_type='application/xml')