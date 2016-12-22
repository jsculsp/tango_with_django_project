from django import template
from rango.models import Category
from datetime import datetime
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}


@register.simple_tag(takes_context=True)
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