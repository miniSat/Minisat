from django import template

register = template.Library()


@register.simple_tag
def update_value(arg1, arg2):
    arg1 = arg2
    return arg1
