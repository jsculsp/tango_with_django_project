from datetime import datetime
import string
import random
import jinja2

from django_jinja import library
from django.utils.safestring import mark_safe
from rango.models import Category

# Here are filters:

@library.filter
@jinja2.contextfilter
def replace(context, value, x, y):
    """
    Filter with template context. Usage: {{ 'Hello'|replace('H','M') }}
    """
    return value.replace(x, y)


@library.filter(name='times')
def times(number):
    return range(number)


# Below are template tags:

@library.global_function(name='current_time')
@jinja2.contextfunction
def current_time(context, format_string):
    # 这里用 mark_safe 函数，防止 datetime.now().strftime(format_string) 自动转义
    # https://docs.djangoproject.com/en/1.10/ref/utils/#django.utils.safestring.mark_safe 相关文档
    format_time = datetime.now().strftime(format_string)
    data = '{} for {}'.format(format_time, context['user'])
    return mark_safe(data)


@library.global_function(name='random_color')
def random_color():
    choices = string.digits + string.ascii_uppercase[:6]
    str1 = '#'
    for i in range(6):
        str1 += random.choice(choices)
    return str1


@library.global_function
@library.render_with('jinja_test/current_time_list.html')
@jinja2.contextfunction
def get_current_time_list(context):
    return {
        'user': context['user'],
    }


@library.global_function
@library.render_with('jinja_test/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}


@library.global_function
def br_num(num):
    s = ''
    for i in range(num):
        s += '<br> \n'
    return mark_safe(s)