from datetime import datetime
import string
import random

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from utils import log

from rango.models import Category

register = template.Library()


@register.inclusion_tag('templatetags/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}


@register.simple_tag(takes_context=True, name='current_time')
def current_time(context, format_string):
    # 这里用 mark_safe 函数，防止 datetime.now().strftime(format_string) 自动转义
    # https://docs.djangoproject.com/en/1.10/ref/utils/#django.utils.safestring.mark_safe 相关文档
    format_time = datetime.now().strftime(format_string)
    data = '{} for {}'.format(format_time, context['user'])
    return mark_safe(data)

    # This is similar to str.format(), except that it is appropriate for building up HTML fragments.
    # All args and kwargs are passed through conditional_escape() before being passed to str.format().
    # return format_html('{}',
    #     mark_safe(datetime.now().strftime(format_string))
    # )


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag(name='random_color')
def random_color():
    choices = string.digits + string.ascii_uppercase[:6]
    str1 = '#'
    for i in range(6):
        str1 += random.choice(choices)
    return str1


@register.inclusion_tag('templatetags/current_time_list.html', takes_context=True, name='get_current_time_list')
def get_current_time_list(context):
    return {
        'user': context['user'],
    }