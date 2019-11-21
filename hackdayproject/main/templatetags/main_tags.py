from django import template

register = template.Library()


@register.filter
def get_type(value):
    return value.__class__.__name__


@register.filter
def split_string(value):
    return value.split("\n")
