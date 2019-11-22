from django import template
from hackdayproject.utils.util_function import calculate_current_streak

register = template.Library()


@register.filter
def get_type(value):
    return value.__class__.__name__


@register.filter
def split_string(value):
    return value.split("\n")


@register.filter
def get_user_current_streak(repos):
    return calculate_current_streak(repos)
