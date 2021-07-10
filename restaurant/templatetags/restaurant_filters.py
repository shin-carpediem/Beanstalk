from django import template


register = template.Library()


@register.simple_tag
def multiply(val1, val2):
    return val1 * val2


# TODO:
@register.simple_tag
def sum(val, *args, **kwargs):
    return int(val) + int(**args) + int(**kwargs)
