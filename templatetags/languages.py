from django import template
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag
def current_language():
    return get_language()