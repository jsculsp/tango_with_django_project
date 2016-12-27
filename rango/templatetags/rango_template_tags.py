from datetime import datetime
import string
import random
import re

from django import template
from django.utils.safestring import mark_safe

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


@register.tag('format_time')
def do_format_time(parse, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, date_to_be_formatted, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires exactly two arguments' % token.contents.split()[0]
        )
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            '%r tag\'s argument should be in quotes' % tag_name
        )
    return FormatTimeNode(date_to_be_formatted, format_string[1: -1])


@register.tag('customed_current_time')
def do_current_time(parser, token):
    # This version users a  regular expression to parse tag contents.
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires arguments' % token.contents.split()[0]
        )
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError('%r tag has invalid arguments' % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ("'", '"')):
        raise template.TemplateSyntaxError(
            '%r tag\'s argument should be in quotes' % tag_name
        )
    return CurrentTimeNode(format_string[1:-1], var_name)


@register.tag('comment')
def do_comment(parser, token):
    nodelist = parser.parse(('endcomment', ))
    parser.delete_first_token()
    return CommentNode()


@register.tag('upper')
def do_upper(parser, token):
    nodelist = parser.parse(('endupper', ))
    parser.delete_first_token()
    return UpperNode(nodelist)


class FormatTimeNode(template.Node):
    def __init__(self, date_to_be_formatted, format_string):
        self.date_to_be_formatted = template.Variable(date_to_be_formatted)
        self.format_string = format_string

    def render(self, context):
        try:
            actual_date = self.date_to_be_formatted.resolve(context)
            return actual_date.strftime(self.format_string)
        except template.VariableDoesNotExist:
            return ''


class CurrentTimeNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = datetime.now().strftime(self.format_string)
        return ''


class CommentNode(template.Node):
    def render(self, context):
        return ''


class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()